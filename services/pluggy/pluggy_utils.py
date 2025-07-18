from pluggy_client import listar_contas
from loguru import logger
import os

ITEM_ID = os.getenv("ITEM_ID", "")


def list_accounts():
    if not ITEM_ID:
        raise ValueError("ITEM_ID not set in environment variables.")

    if not (contas := listar_contas(ITEM_ID)):
        raise ValueError("No accounts found for the provided ITEM_ID.")

    for c in contas:
        logger.info(f"ID: {c.id}, Conta: {c.name}, Saldo: {c.balance}")


if __name__ == "__main__":
    list_accounts()
