import os
from dotenv import load_dotenv
from pluggy_sdk import AuthApi, AccountApi, TransactionApi
from pluggy_sdk import Configuration, ApiClient

load_dotenv()
cfg = Configuration(host="https://api.pluggy.ai")
cfg.api_key["default"] = ""

# autenticar e atualizar key
with ApiClient(cfg) as client:
    auth = AuthApi(client)
    resp = auth.auth_create(
        {"clientId": os.getenv("CLIENT_ID"), "clientSecret": os.getenv("CLIENT_SECRET")}
    )
    cfg.api_key["default"] = resp.api_key


def listar_contas(item_id):
    with ApiClient(cfg) as client:
        return AccountApi(client).accounts_list(item_id).results


def listar_transacoes(item_id):
    with ApiClient(cfg) as client:
        return TransactionApi(client).transactions_list(item_id)
