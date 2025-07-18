from services.db import FinanceDB
from services.etl import extract_extrato, extract_fatura
from services.tagging import sugerir_rotulos
from schemas import FinanceEntrySchema
from .pluggy_client import listar_transacoes
import pandas as pd
from datetime import datetime
from pytz import timezone


def transactions_to_dataframe(transactions):
    data = [
        {
            "Data": t.date,
            "Valor": t.amount,
            "Descricao": t.description,
        }
        for t in transactions
        if t
    ]

    return pd.DataFrame(data)


def sync_acc(acc_id, acc_name, open_finance_id, finances):
    filtered_finances = finances[finances["conta"] == acc_id].copy()
    filtered_finances["conta"] = acc_name

    filtered_finances["data"] = pd.to_datetime(
        filtered_finances["data"], format="%Y-%m-%d %H:%M:%S"
    )
    # set timezone to America/Sao_Paulo
    filtered_finances["data"] = filtered_finances["data"].dt.tz_localize(
        "America/Sao_Paulo"
    )

    last_date = filtered_finances["data"].max()
    filtered_finances = filtered_finances[filtered_finances["data"] >= last_date]

    transactions = listar_transacoes(open_finance_id, var_from=last_date)
    new_df = transactions_to_dataframe(transactions)
    print(new_df)
    for _, row in filtered_finances.iterrows():
        mask = (
            (new_df["Data"] == row["data"])
            & (new_df["Valor"] == row["valor"])
            & (new_df["Descricao"] == row["descricao"])
        )
    if mask.any():
        index_to_drop = new_df[mask].index[0]
        new_df = new_df.drop(index_to_drop)

    if new_df.empty:
        print("No new transactions found.")
        return pd.DataFrame()

    new_df["Valor"] = new_df["Valor"].apply(lambda x: str(x).replace(".", ","))
    extracted_df = extract_extrato(new_df)
    extracted_df["Conta"] = acc_id
    entries = []
    for _, row in extracted_df.iterrows():
        rotulos = sugerir_rotulos(
            row["Data"], row["Valor"], row["Destino / Origem"], row["Descricao"]
        )

        entries.append(
            FinanceEntrySchema(
                **{
                    "Data": row["Data"].replace(tzinfo=None),
                    "Valor": row["Valor"],
                    "Destino / Origem": row["Destino / Origem"],
                    "Descricao": row["Descricao"],
                    "Tipo": rotulos.get("Tipo", ""),
                    "Categoria": rotulos.get("Categoria", ""),
                    "Subcategoria": rotulos.get("Subcategoria", ""),
                    "Nome": rotulos.get("Nome", ""),
                    "Conta": acc_id,
                    "Notas": rotulos.get("Notas", ""),
                    "need_tagging": True,
                },
            )
        )

    return pd.DataFrame([e.model_dump(by_alias=True) for e in entries])


def sync():
    db = FinanceDB()
    finances = db.get_financas()
    accounts = db.get_accounts()

    for _, acc in accounts.iterrows():
        if acc["is_credit"]:
            print(f"Skipping credit account: {acc['nome']}")
            continue

        df = sync_acc(acc["id"], acc["nome"], acc["open_finance_id"], finances)
        db.add_df_entries(df)
