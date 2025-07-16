import streamlit as st
from services.db import FinanceDB
from services.utils import money
import pandas as pd


db = FinanceDB()
accounts = db.get_accounts()
financas = db.get_financas()


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


valor_total = financas["valor"].sum()
valores_iniciais = accounts["saldo_inicial"].sum()
valor_total += valores_iniciais

st.markdown(
    "<h1 style='color:#4CAF50; font-size: 2.5rem;'>📊 Resumo Financeiro</h1>",
    unsafe_allow_html=True,
)

# Cores condicionais para o valor total
cor_total = "#c62828" if valor_total < 0 else "#2e7d32"
fundo_total = "#ffebee" if valor_total < 0 else "#e8f5e9"

# Bloco do valor total com cor dinâmica
st.markdown(
    f"""
    <div style='padding: 1rem; background-color: {fundo_total}; border-radius: 10px; text-align: center;'>
        <h2 style='color: #388e3c;'>💰 Valor Total</h2>
        <p style='font-size: 2rem; color: {cor_total}; font-weight: bold;'>{money(valor_total)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 💼 Valor por Conta")

valor_por_conta = get_value_per_account(financas, accounts)
cols = st.columns(len(valor_por_conta))

# Bloco de contas com cor condicional
for col, (account, value) in zip(cols, valor_por_conta.items()):
    cor_valor = "#c62828" if value < 0 else "#33691e"
    cor_fundo = "#ffebee" if value < 0 else "#f1f8e9"

    col.markdown(
        f"""
        <div style='background-color: {cor_fundo}; padding: 1rem; border-radius: 10px; text-align: center;'>
            <h4 style='color: #558b2f; margin-bottom: 0.5rem;'>{account}</h4>
            <p style='font-size: 1.3rem; font-weight: bold; color: {cor_valor};'>{money(value)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
