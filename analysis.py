from database import FinanceDB
import pandas as pd

db = FinanceDB()


def get_value_per_account(
    financas: pd.DataFrame, accounts: pd.DataFrame
) -> pd.DataFrame:
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


def main():

    financas = db.get_financas()
    accounts = db.get_accounts()

    if financas.empty:
        print("Nenhuma entrada financeira encontrada.")
        return

    # get valor total

    valor_total = financas["valor"].sum()
    valores_iniciais = accounts["saldo_inicial"].sum()
    valor_total += valores_iniciais

    print(f"Valor total: {valor_total:.2f}")

    "Valor per conta"
    print("\nValor por conta:")
    print(get_value_per_account(financas, accounts))


if __name__ == "__main__":
    main()
