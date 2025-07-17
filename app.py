# import streamlit as st
# from services.values_service import get_values
# from services.utils import money
# import os

# if os.path.exists("style.css"):
#     with open("style.css", "r") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # Dados
# saldo_total, saldo_por_conta = get_values()
# # --- CABEÇALHO ---
# st.markdown(
#     "<h1 style='color:#2E7D32; text-align:center;'>📊 Resumo Financeiro</h1>",
#     unsafe_allow_html=True,
# )
# st.markdown("---")

# # --- CARD VALOR TOTAL ---
# tipo = "negativo" if saldo_total < 0 else "positivo"

# st.markdown(
#     f"""
#     <div class="card" style="background-color:#f9f9f9;">
#         <h2>💰 Saldo Total</h2>
#         <div class="valor-total {tipo}">{money(saldo_total)}</div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # --- SEÇÃO VALORES POR CONTA ---
# st.markdown("### 💼 Saldo por Conta")
# cols = st.columns(len(saldo_por_conta))

# for col, (account, value) in zip(cols, saldo_por_conta.items()):
#     tipo = "negativo" if value < 0 else "positivo"
#     col.markdown(
#         f"""
#         <div class="card">
#             <h2>{account}</h2>
#             <div class="valor-conta {tipo}">{money(value)}</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


import streamlit as st
from pluggy_client import listar_contas, listar_transacoes

st.title("💸 Meu Financeiro com Pluggy")


st.info("Use este Connect Token no widget:", icon="🔑")

if item_id := st.text_input("Cole aqui o item_id após conectar a conta"):
    contas = listar_contas(item_id)
    trans = listar_transacoes(item_id)

    st.subheader("🏦 Contas")
    for a in contas:
        st.write(a)

    st.subheader("💳 Transações")
    for t in trans[:10]:
        st.write(t)
