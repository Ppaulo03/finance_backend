import streamlit as st
import pandas as pd
from services.db import FinanceDB
from services.analises import *
from services.prophet_service import prever_gastos

st.set_page_config(layout="wide")
st.title("📈 Análises Financeiras")

# 📥 Dados
db = FinanceDB()
df = db.get_financas()
df["data"] = pd.to_datetime(df["data"])

if df.empty:
    st.warning("Sem dados para análise.")
    st.stop()

# 🎛️ Filtros globais
st.sidebar.header("Filtros")
categorias_disponiveis = sorted(
    df[df["tipo"] == "Gasto"]["categoria"].dropna().unique()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Categorias", categorias_disponiveis, default=categorias_disponiveis
)

min_date = df["data"].min().date()
max_date = df["data"].max().date()
data_ini, data_fim = st.sidebar.date_input("Período", value=(min_date, max_date))

# 🔄 Aplicar filtros
df_filtrado = df.copy()
df_filtrado = df_filtrado[
    (df_filtrado["categoria"].isin(categorias_selecionadas))
    | (df_filtrado["tipo"].isin(["Recebimento"]))
]
df_filtrado = df_filtrado[
    (df_filtrado["data"].dt.date >= data_ini)
    & (df_filtrado["data"].dt.date <= data_fim)
]

if df_filtrado.empty:
    st.warning("Nenhuma transação encontrada com os filtros aplicados.")
    st.stop()

# 🔍 Seleção da análise
analise = st.sidebar.selectbox(
    "Escolha a análise",
    [
        "Pizza de Gastos",
        "Gastos por Categoria",
        "Gastos por Semana",
        "Previsão de Gastos",
        "Comparativo Gasto vs Receita",
    ],
)

# 📊 Renderizar gráfico
if analise == "Gastos por Categoria":
    st.subheader("🧮 Gastos por Categoria")
    st.pyplot(gastos_por_categoria(df_filtrado), use_container_width=False)

elif analise == "Gastos por Semana":
    st.subheader("📊 Evolução Semanal")
    fig, semana_df = gastos_por_semana(df_filtrado)
    st.pyplot(fig, use_container_width=False)

elif analise == "Previsão de Gastos":
    st.subheader("🔮 Previsão de Gastos")

    _, semana_df = gastos_por_semana(df_filtrado)
    if len(semana_df) < 5:
        st.warning("Poucos dados semanais para previsão.")
    else:
        fig_forecast, forecast = prever_gastos(semana_df)
        st.plotly_chart(fig_forecast, use_container_width=True)

elif analise == "Pizza de Gastos":
    st.subheader("📊 Porcentagem dos Gastos por Categoria")
    st.pyplot(pizza_gastos_por_categoria(df_filtrado), use_container_width=False)

elif analise == "Comparativo Gasto vs Receita":
    st.subheader("⚖️ Comparativo entre Gastos e Receitas")
    st.pyplot(comparativo_gasto_receita(df_filtrado), use_container_width=False)
