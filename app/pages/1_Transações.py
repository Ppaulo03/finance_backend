import streamlit as st
import pandas as pd
from services.utils import money
from services.db import FinanceDB

import locale

locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

st.title("📄 Transações")

# 🔹 Carregar dados
db = FinanceDB()
df = db.get_financas()
accounts = db.get_accounts()

# 🔎 Filtros
st.sidebar.header("Filtros")

df["data"] = pd.to_datetime(df["data"])
data_min = df["data"].min().replace(day=1)
data_max = df["data"].max().replace(day=1)
todos_meses = pd.date_range(start=data_min, end=data_max, freq="MS")
meses_formatados = todos_meses.strftime("%B %Y").tolist()
meses_formatados = meses_formatados[::-1]

if "mes_index" not in st.session_state:
    st.session_state.mes_index = 0


def mes_anterior():
    if st.session_state.mes_index < len(meses_formatados) - 1:
        st.session_state.mes_index += 1


def mes_proximo():
    if st.session_state.mes_index > 0:
        st.session_state.mes_index -= 1


def update_mes_index():
    mes_selecionado = st.session_state["mes_select"]
    novo_indice = meses_formatados.index(mes_selecionado)
    st.session_state.mes_index = novo_indice


col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.button("◀️", on_click=mes_anterior)
with col2:
    st.markdown(f"### {meses_formatados[st.session_state.mes_index]}")
with col3:
    st.button("▶️", on_click=mes_proximo)


mes_selecionado = st.sidebar.selectbox(
    "Mês",
    options=meses_formatados,
    index=st.session_state.mes_index,
    on_change=update_mes_index,
    args=(),
    key="mes_select",
)
periodo_selecionado = pd.to_datetime(mes_selecionado, format="%B %Y").to_period("M")


# 🔹 Tipo
tipos = df["tipo"].dropna().unique().tolist()
tipo = st.sidebar.multiselect("Tipo", tipos, default=tipos)


# 🔹 Conta
df["conta"] = df["conta"].map(
    lambda x: (
        "Desconhecida"
        if accounts[accounts["id"] == x].empty
        else accounts.loc[accounts["id"] == x, "nome"].values[0]
    )
)
contas = df["conta"].dropna().unique().tolist()
conta = st.sidebar.multiselect("Conta", contas, default=contas)

# 🔹 Busca por nome
nome_busca = st.sidebar.text_input("Buscar por nome")

# 🔽 Aplicar filtros
df_filtrado = df[
    (df["data"].dt.to_period("M") == periodo_selecionado)
    & (df["tipo"].isin(tipo))
    & (df["conta"].isin(conta))
]

if nome_busca:
    df_filtrado = df_filtrado[
        df_filtrado["nome"].str.contains(nome_busca, case=False, na=False)
    ]

# Resumo em cards
total_gastos = -df_filtrado[df_filtrado["tipo"] == "Gasto"]["valor"].sum()
total_receitas = df_filtrado[df_filtrado["tipo"] == "Recebimento"]["valor"].sum()

col1, col2 = st.columns(2)
col1.metric("💸 Total de Gastos", money(total_gastos))
col2.metric("💰 Total de Receitas", money(total_receitas))


def style_valor(val, tipo):
    if tipo == "Transferência":
        return "color: #3498db; font-weight: bold"  # azul
    elif val < 0:
        return "color: #e74c3c; font-weight: bold"  # vermelho
    else:
        return "color: #2ecc71; font-weight: bold"  # verde


df_style_base = df_filtrado[
    ["data", "nome", "valor", "categoria", "conta", "tipo"]
].copy()
df_style_base = df_style_base.sort_values(by="data", ascending=False)

# Remove 'tipo' da visualização
df_display = df_style_base.copy()


def apply_style(row):
    color = style_valor(row["valor"], row["tipo"])
    return [
        None,
        None,
        color,
        None,
        None,
        color,
    ]  # aplica estilo apenas na coluna 'valor'


# Aplica estilo
styled_df = (
    df_display.style.format(
        {
            "valor": "R$ {:,.2f}",
            "data": lambda d: d.strftime("%d/%m/%Y"),
        }
    )
    .apply(apply_style, axis=1)
    .set_properties(
        subset=["data", "nome", "valor", "categoria", "conta"],
        **{
            "text-align": "left",
            "padding": "8px 12px",
            "font-size": "14px",
        },
    )
    .set_table_styles(
        [{"selector": "th", "props": [("text-align", "left"), ("font-size", "15px")]}]
    )
).hide(axis="index")

st.dataframe(styled_df, use_container_width=True, height=600)
