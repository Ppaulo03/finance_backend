import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from schemas import FinanceEntrySchema, rotulos_schema

from services.etl import extract_data
from services.tagging import sugerir_rotulos
import os


url_base = os.getenv("LOCAL_URL", "http://127.0.0.1:3000")
if "financas" not in st.session_state or "accounts" not in st.session_state:
    response = requests.get(f"{url_base}/financas").json()
    st.session_state.financas = response["financas"]
    st.session_state.accounts = response["accounts"]

financas = st.session_state.financas
accounts = st.session_state.accounts


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
    st.session_state.upload_key = f"upload_{datetime.now().timestamp()}"

st.set_page_config(layout="wide")


tipos = list(rotulos_schema.keys())
st.title("📘 Controle Financeiro")

if not st.session_state.adicionando_csv:
    if uploaded_file := st.file_uploader(
        "📥 Enviar arquivo CSV de transações",
        type=["csv"],
        key=st.session_state.upload_key,
    ):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        st.session_state.adicionando_csv = True
        response = requests.post(f"{url_base}/tag_financas", files=files).json()
        st.session_state.tagged_csv = response["tagged"]
        st.session_state["atual"] = 0
        st.session_state["processados"] = []

if st.session_state.adicionando_csv:
    csv = st.session_state.tagged_csv
    idx = st.session_state["atual"]
    if idx < len(csv):
        row = csv[idx]
        df = pd.DataFrame([row])
        st.markdown(f"### Transação {st.session_state['atual'] + 1}/{len(csv)}")
        st.write(
            df.loc[
                [st.session_state["atual"]],
                ["data", "valor", "destino_origem", "descricao"],
            ]
        )

        if len(st.session_state["processados"]) <= idx:
            rotulos = {
                "Tipo": row["tipo"],
                "Categoria": row["categoria"],
                "Subcategoria": row["subcategoria"],
                "Nome": row["nome"],
                "Notas": row["notas"],
            }

        else:
            rotulos = {
                "Tipo": st.session_state["processados"][idx].tipo,
                "Categoria": st.session_state["processados"][idx].categoria,
                "Subcategoria": st.session_state["processados"][idx].subcategoria,
                "Nome": st.session_state["processados"][idx].nome,
                "Notas": st.session_state["processados"][idx].notas,
            }

        tipo_suggetion = rotulos.get("Tipo", "Gasto")
        categoria_suggestion = rotulos.get("Categoria", "")
        subcategoria_suggestion = rotulos.get("Subcategoria", "")
        nome_suggestion = rotulos.get("Nome", "")
        notas_sugestion = rotulos.get("Notas", "")

        accounts_names = [acc["nome"] for acc in accounts]
        conta = st.selectbox(
            "Conta",
            accounts_names,
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

        nome = st.text_input("Nome", value=nome_suggestion, key=f"nome_input_{idx}")
        notas = st.text_area("Notas", key=f"notas_input_{idx}", value=notas_sugestion)

        btn_col_1, btn_col_2 = st.columns(2)
        with btn_col_1:
            if st.button("Próximo"):
                if (
                    not tipo
                    or not categoria
                    or not subcategoria
                    or not nome
                    or not conta
                ):
                    st.error("Por favor, preencha todos os campos obrigatórios.")
                else:

                    entry = FinanceEntrySchema(
                        **{
                            "Data": row["Data"],
                            "Valor": row["Valor"],
                            "Destino / Origem": row["Destino / Origem"],
                            "Descricao": row["Descricao"],
                            "Tipo": tipo,
                            "Categoria": categoria,
                            "Subcategoria": subcategoria,
                            "Nome": nome,
                            "Conta": accounts[accounts["nome"] == conta]["id"].values[
                                0
                            ],
                            "Notas": notas,
                        },
                    )
                    if len(st.session_state["processados"]) <= idx:
                        st.session_state["processados"].append(entry)
                    else:
                        st.session_state["processados"][idx] = entry

                    st.session_state["atual"] += 1
                    st.rerun()

        with btn_col_2:
            if idx > 0 and st.button("Anterior"):
                st.session_state["atual"] -= 1
                st.rerun()

        if st.button("Cancelar"):
            st.session_state.adicionando_csv = False
            st.session_state.upload_key = f"upload_{datetime.now().timestamp()}"
            st.session_state["atual"] = 0
            st.session_state["processados"] = []
            st.rerun()

    else:
        st.dataframe(
            pd.DataFrame(
                [
                    e.model_dump(exclude=["id"], by_alias=True)
                    for e in st.session_state["processados"]
                ]
            )
        )
        st.success("Todas as transações foram processadas.")

        if st.button("Enviar para o banco de dados"):
            # db.add_df_entries(
            #     pd.DataFrame(
            #         [
            #             e.model_dump(by_alias=True)
            #             for e in st.session_state["processados"]
            #         ]
            #     )
            # )
            # st.session_state.upload_key = f"upload_{datetime.now().timestamp()}"
            st.session_state.adicionando_csv = False
            st.session_state["atual"] = 0
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
