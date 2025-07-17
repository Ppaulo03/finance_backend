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

min_date = df["data"].min()
max_date = df["data"].max()

data_ini = st.sidebar.date_input(
    "Data inicial", value=min_date, min_value=min_date, max_value=max_date
)

data_fim = st.sidebar.date_input(
    "Data final", value=max_date, min_value=min_date, max_value=max_date
)

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

analise = st.sidebar.selectbox(
    "Escolha a análise",
    [
        "Tendências de Gastos",
        "Gastos por Semana",
        "Gastos por Categoria",
        "Gastos Recorrentes",
        "Pizza de Gastos",
        "Comparativo Gasto vs Receita",
        "Análise de Trend",
        "Previsão de Gastos",
    ],
)

if analise == "Gastos por Categoria":
    st.subheader("🧮 Gastos por Categoria")
    st.pyplot(gastos_por_categoria(df_filtrado), use_container_width=False)

elif analise == "Análise de Trend":
    st.subheader("📊 Análise de Trend")
    fig_trend = trend_analysis(df_filtrado)
    st.pyplot(fig_trend, use_container_width=False)

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

elif analise == "Tendências de Gastos":
    st.subheader("📈 Tendências de Gastos Totais")
    fig_tendencia = tendencia_gastos_totais(df_filtrado)
    st.pyplot(fig_tendencia, use_container_width=False)

elif analise == "Gastos Recorrentes":
    st.subheader("🔄 Gastos Recorrentes")
    df_recorrentes = gastos_recorrentes(df_filtrado)
    if df_recorrentes.empty:
        st.warning("Nenhum gasto recorrente encontrado.")
    else:
        st.dataframe(df_recorrentes)
