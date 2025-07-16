import streamlit as st
import pandas as pd
from services.db import FinanceDB

st.set_page_config(layout="wide")
st.title("📋 Visualização de Transações")

db = FinanceDB()
df = db.get_financas()
accounts = db.get_accounts()

if df.empty:
    st.warning("Nenhuma transação encontrada.")
    st.stop()
df = df[["data", "valor", "nome", "tipo", "categoria", "subcategoria", "conta"]]

# change id to account name
df["conta"] = df["conta"].map(
    lambda x: (
        "Desconhecida"
        if accounts[accounts["id"] == x].empty
        else accounts.loc[accounts["id"] == x, "nome"].values[0]
    )
)

# 🔍 Filtros
st.sidebar.header("Filtros")
tipo = st.sidebar.selectbox("Tipo", ["Todos"] + df["tipo"].unique().tolist())
conta = st.sidebar.selectbox(
    "Conta", ["Todas"] + df["conta"].astype(str).unique().tolist()
)

df["data"] = pd.to_datetime(df["data"])
data_ini = st.sidebar.date_input("De", value=df["data"].min().date())
data_fim = st.sidebar.date_input("Até", value=df["data"].max().date())

# Aplicar filtros
filtrado = df.copy()
if tipo != "Todos":
    filtrado = filtrado[filtrado["tipo"] == tipo]
if conta != "Todas":
    filtrado = filtrado[filtrado["conta"].astype(str) == conta]
filtrado = filtrado[
    (filtrado["data"].dt.date >= data_ini) & (filtrado["data"].dt.date <= data_fim)
]

st.subheader(f"🧾 {len(filtrado)} transações encontradas")
st.dataframe(
    filtrado.sort_values(by="data", ascending=False).reset_index(drop=True),
    use_container_width=True,
)
