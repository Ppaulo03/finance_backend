from services.db import FinanceDB
import streamlit as st
from services.values_service import get_values
from services.utils import money
import os

if os.path.exists("style.css"):
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "df_financas" not in st.session_state or "df_accounts" not in st.session_state:
    db = FinanceDB()
    st.session_state.df_financas = db.get_financas()
    st.session_state.df_accounts = db.get_accounts()

df = st.session_state.df_financas.copy()
accounts = st.session_state.df_accounts.copy()

# Dados
saldo_total, saldo_por_conta = get_values(df, accounts)
# --- CABEÇALHO ---
st.markdown(
    "<h1 style='color:#2E7D32; text-align:center;'>📊 Resumo Financeiro</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- CARD VALOR TOTAL ---
tipo = "negativo" if saldo_total < 0 else "positivo"

st.markdown(
    f"""
    <div class="card" style="background-color:#f9f9f9;">
        <h2>💰 Saldo Total</h2>
        <div class="valor-total {tipo}">{money(saldo_total)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- SEÇÃO VALORES POR CONTA ---
st.markdown("### 💼 Saldo por Conta")
cols = st.columns(len(saldo_por_conta))

for col, (account, value) in zip(cols, saldo_por_conta.items()):
    tipo = "negativo" if value < 0 else "positivo"
    col.markdown(
        f"""
        <div class="card">
            <h2>{account}</h2>
            <div class="valor-conta {tipo}">{money(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
