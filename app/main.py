import streamlit as st
import pandas as pd
from datetime import datetime
from schemas import FinanceEntrySchema, Account, rotulos_schema
from services.db import FinanceDB
from services.utils import money
from services.etl import extract_data
from services.tagging import sugerir_rotulos


def reset_categoria_subcategoria():
    if "atual" not in st.session_state:
        return
    idx = st.session_state["atual"]

    st.session_state[f"categoria_{idx}"] = None
    st.session_state[f"subcategoria_{idx}"] = None


def reset_subcategoria():
    if "atual" not in st.session_state:
        return
    idx = st.session_state["atual"]
    st.session_state[f"subcategoria_{idx}"] = None


if "adicionando_csv" not in st.session_state:
    st.session_state.adicionando_csv = False

if "upload_key" not in st.session_state:
    st.session_state.upload_key = "upload_1"

st.set_page_config(layout="wide")
db = FinanceDB()

tipos = list(rotulos_schema.keys())
st.title("📘 Controle Financeiro - MVP")

if not st.session_state.adicionando_csv:
    uploaded_file = st.file_uploader(
        "📥 Enviar arquivo CSV de transações",
        type=["csv"],
        key=st.session_state.upload_key,
    )

    if uploaded_file:
        df = extract_data(uploaded_file)
        st.session_state.adicionando_csv = True
        st.session_state.setdefault("processados", [])
        st.session_state.setdefault("atual", 0)
        st.session_state.df_csv = df
        st.rerun()

if st.session_state.adicionando_csv:
    df = st.session_state.df_csv
    idx = st.session_state["atual"]
    if idx < len(df):
        row = df.iloc[st.session_state["atual"]]
        st.markdown(f"### Transação {st.session_state['atual'] + 1}/{len(df)}")
        # st.write(row[["Data", "Valor", "Destino / Origem", "Descricao"]])

        rotulos = sugerir_rotulos(
            row["Data"], row["Valor"], row["Destino / Origem"], row["Descricao"]
        )

        tipo_suggetion = rotulos.get("Tipo", "Gasto")
        categoria_suggestion = rotulos.get("Categoria", "")
        subcategoria_suggestion = rotulos.get("Subcategoria", "")
        nome_suggestion = rotulos.get("Nome", "")

        conta = st.selectbox(
            "Conta",
            db.get_accounts()["nome"].tolist(),
            index=0,
            key="conta_select",
        )

        col1, col2, col3 = st.columns(3)
        with col1:

            tipo = st.selectbox(
                "Tipo",
                tipos,
                index=tipos.index(tipo_suggetion) if tipo_suggetion in tipos else 0,
                key=f"tipo_select_{idx}",
                on_change=reset_categoria_subcategoria,
            )

        with col2:
            if tipo:
                categorias = list(rotulos_schema[tipo].keys())
                categoria = st.selectbox(
                    "Categoria",
                    categorias,
                    index=(
                        categorias.index(categoria_suggestion)
                        if categoria_suggestion in categorias
                        else 0
                    ),
                    key=f"categoria_{idx}",
                    on_change=reset_subcategoria,
                )

        with col3:
            if categoria:
                subcategorias = rotulos_schema[tipo][categoria]
                subcategoria = st.selectbox(
                    "Subcategoria",
                    subcategorias,
                    index=(
                        subcategorias.index(subcategoria_suggestion)
                        if subcategoria_suggestion in subcategorias
                        else 0
                    ),
                    key=f"subcategoria_{idx}",
                )

        nome = st.text_input("Nome", value=nome_suggestion, key="nome_input")
        notas = st.text_area("Notas", key="notas_input")

        if st.button("Próximo"):
            if not tipo or not categoria or not subcategoria or not nome or not conta:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # entry = FinanceEntrySchema(
                #     id=0,
                #     data=row["data"],
                #     valor=row["valor"],
                #     destino_origem=row.get("destino_origem", ""),
                #     descricao=row.get("descricao", ""),
                #     tipo=tipo,
                #     categoria=categoria,
                #     subcategoria=subcategoria,
                #     nome=nome,
                #     conta=conta,
                #     notas=row.get("notas", ""),
                # )

                # db.insert_financa(entry)
                # st.success("Transação salva com sucesso!")

                # st.session_state["processados"].append(entry)
                st.session_state["atual"] += 1
                st.rerun()

    else:
        st.success("Todas as transações foram processadas.")
        st.session_state["atual"] = 0
        if st.button("Adicionar mais CSV"):
            st.dataframe(
                pd.DataFrame([e.model_dump() for e in st.session_state["processados"]])
            )
            st.session_state.adicionando_csv = False
            st.session_state.upload_key = f"upload_{datetime.now().timestamp()}"
            st.rerun()


# st.subheader("📊 Tabela de Transações")
# df_financas = db.get_financas()
# df_contas = db.get_accounts()
# df_financas["valor"] = df_financas["valor"].apply(money)
# df_financas["conta"] = df_financas["conta"].apply(
#     lambda x: df_contas[df_contas["id"] == x]["nome"].values[0]
# )
# st.dataframe(
#     df_financas[
#         ["data", "conta", "valor", "tipo", "nome", "categoria", "subcategoria", "notas"]
#     ],
# )
