from pluggy_client import listar_contas, listar_transacoes
import os

ACCOUNT_ID = os.getenv("ACCOUNT_ID", "")
if not ACCOUNT_ID:
    if not (ITEM_ID := os.getenv("ITEM_ID", "")):
        raise ValueError("ITEM_ID not set in environment variables.")

    if contas := listar_contas(ITEM_ID):
        for c in contas:
            print(c)
        ACCOUNT_ID = contas[0].id
    else:
        raise ValueError("Conta não encontrada.")
