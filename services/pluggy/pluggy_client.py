import os
import requests
from dotenv import load_dotenv
from schemas.pluggy_transaction_schema import PluggyTransactionSchema
from datetime import datetime, timedelta

load_dotenv()
url_base = r"https://api.pluggy.ai/"


def get_auth():
    headers = {"accept": "application/json", "content-type": "application/json"}
    data = {
        "clientId": os.getenv("CLIENT_ID"),
        "clientSecret": os.getenv("CLIENT_SECRET"),
    }
    response = requests.post(f"{url_base}/auth", headers=headers, json=data)

    if response.status_code != 200:
        print(response.text)
        return ""
    return response.json()["apiKey"]


def listar_transacoes(account_id, var_from=None, var_to=None, page=None):
    if not var_from:
        var_from = datetime.now() - timedelta(days=30)
    if not var_to:
        var_to = datetime.now()

    headers = {"accept": "application/json", "X-API-KEY": get_auth()}
    query_params = {
        "accountId": account_id,
        "page": page or 1,
    }
    url = f"{url_base}/transactions?" + "&".join(
        [f"{k}={v}" for k, v in query_params.items()]
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.text)
        return []

    results = response.json()["results"]
    results = [PluggyTransactionSchema(**r) for r in results]
    total_pages = response.json()["totalPages"]
    if not page and total_pages > 1:
        for i in range(2, total_pages + 1):
            results += listar_transacoes(
                account_id, var_from=var_from, var_to=var_to, page=i
            )

    return results


# def listar_contas(item_id):

#     with ApiClient(cfg) as client:
#         return AccountApi(client).accounts_list(item_id).results


# def listar_transacoes(item_id, var_from=None, var_to=None, page=None):
#     if not var_from:
#         var_from = datetime.now() - timedelta(days=30)
#     if not var_to:
#         var_to = datetime.now()

#     with ApiClient(cfg) as client:
#         transactions = TransactionApi(client).transactions_list(
#             item_id, var_from=var_from, to=var_to, page=page
#         )

#         results = transactions.results if transactions else []
#         if not page and transactions.total_pages > 1:
#             for page in range(2, transactions.total_pages + 1):
#                 results += listar_transacoes(item_id, var_from, var_to, page=page + 1)
#         return results
