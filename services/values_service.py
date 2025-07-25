import pandas as pd


def get_value_per_account(financas: pd.DataFrame, accounts: pd.DataFrame) -> dict:
    """Calcula o valor total por conta."""
    df_financas = financas.groupby("conta")["valor"].sum().reset_index()
    values = {}
    for _, row in df_financas.iterrows():
        acc = accounts[accounts["id"] == row["conta"]]
        if not acc.empty:
            values[acc["nome"].values[0]] = (
                row["valor"] + acc["saldo_inicial"].values[0]
            )
        else:
            values[f"Conta {row['conta']}"] = row["valor"]
    return values


def get_values(financas, accounts) -> tuple[float, dict]:
    """Calcula o valor total e por conta."""
    valor_total = float(financas["valor"].sum() + accounts["saldo_inicial"].sum())
    valor_por_conta = get_value_per_account(financas, accounts)
    return valor_total, valor_por_conta
