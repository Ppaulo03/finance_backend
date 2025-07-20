import streamlit as st
import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from services.utils import money
import os
import locale

locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

st.title("📄 Transações")


url_base = os.getenv("LOCAL_URL", "http://127.0.0.1:3000")
if "financas" not in st.session_state or "accounts" not in st.session_state:
    response = requests.get(f"{url_base}/financas").json()
    st.session_state.financas = response["financas"]
    st.session_state.accounts = response["accounts"]

financas = st.session_state.financas
accounts = st.session_state.accounts

st.sidebar.header("Filtros")

datas = [datetime.fromisoformat(f["data"]) for f in financas]
data_min = min(datas).replace(day=1)
data_max = max(datas).replace(day=1) + relativedelta(months=1)

meses = []
atual = data_min
while atual <= data_max:
    meses.append(atual.strftime("%B %Y"))
    atual += relativedelta(months=1)
meses_formatados = meses[::-1]

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
periodo_selecionado = datetime.strptime(mes_selecionado, "%B %Y")


contas_dict = {c["id"]: c["nome"] for c in accounts}
for f in financas:
    nome_conta = contas_dict.get(f["conta"], "Desconhecida")
    f["conta_nome"] = nome_conta

contas = list(sorted(set(contas_dict.values())))
conta = st.sidebar.multiselect("Conta", contas, default=contas)
selected_ids = [id_ for id_, nome in contas_dict.items() if nome in conta]

tipos = sorted({f["tipo"] for f in financas if f["tipo"]})
tipo = st.sidebar.multiselect("Tipo", tipos, default=tipos)

nome_busca = st.sidebar.text_input("Buscar por nome")

data = {
    "financas": financas,
    "accounts": accounts,
    "mes": mes_selecionado,
    "contas": selected_ids,
    "tipos": tipo,
    "nome_busca": nome_busca,
}
response = requests.post(f"{url_base}/filter_financas", json=data).json()
filtrado = response["filtered"]

total_gastos = response["total_gastos"]
total_receitas = response["total_receitas"]

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


if not filtrado:
    # empty dataframe
    df_filtrado = pd.DataFrame(
        columns=["data", "nome", "valor", "categoria", "subcategoria", "conta", "tipo"]
    )
else:
    df_filtrado = pd.DataFrame(filtrado)
df_style_base = df_filtrado[
    ["data", "nome", "valor", "categoria", "subcategoria", "conta", "tipo"]
].copy()
df_style_base["data"] = pd.to_datetime(df_style_base["data"])
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
