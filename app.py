import requests
import streamlit as st
from services.utils import money
import os


if os.path.exists("style.css"):
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

url_base = os.getenv("LOCAL_URL", "http://127.0.0.1:3000")
if "financas" not in st.session_state or "accounts" not in st.session_state:
    response = requests.get(f"{url_base}/financas").json()
    st.session_state.financas = response["financas"]
    st.session_state.accounts = response["accounts"]

data = {
    "financas": st.session_state.financas,
    "accounts": st.session_state.accounts,
}

# Dados
response = requests.post(f"{url_base}/resume_financas", json=data).json()
saldo_total = response["saldo_total"]
saldo_por_conta = response["saldo_por_conta"]

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
