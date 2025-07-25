from services.db import FinanceDB
from schemas import FinanceEntrySchema, Account
import pandas as pd
from tqdm import tqdm

df = pd.read_csv("data/AllData.csv")

db = FinanceDB()
# db.reset_tables()

# with tqdm(total=len(df)) as pbar:
#     for index, row in df.iterrows():
#         if pd.isna(row["Notas"]):
#             row["Notas"] = ""
#         entry = FinanceEntrySchema(**row)
#         db.insert_financa(entry)
#         pbar.update(1)

# df = pd.read_csv(r"data\accounts.csv")
# with tqdm(total=len(df)) as pbar:
#     for index, row in df.iterrows():
#         entry = Account(
#             nome=row["nome"],
#             saldo_inicial=row["saldo_inicial"],
#             open_finance_id=row["open_finance_id"],
#         )
#         db.insert_account(entry)
#         pbar.update(1)

db.close()


# import pandas as pd
# import os

# raw_path = r"data\backup\raw_data"
# df_extratos = None
# df_faturas = None

# files = os.listdir(raw_path)
# for file in files:
#     if file.endswith(".csv") and file.startswith("extrato"):
#         df = pd.read_csv(os.path.join(raw_path, file), delimiter=";")
#         if df_extratos is None:
#             df_extratos = df
#         else:
#             df_extratos = pd.concat([df_extratos, df], ignore_index=True)

#     elif file.endswith(".csv") and file.startswith("Fatura"):
#         df = pd.read_csv(os.path.join(raw_path, file), delimiter=";")
#         if df_faturas is None:
#             df_faturas = df
#         else:
#             df_faturas = pd.concat([df_faturas, df], ignore_index=True)

# # sort by date
# df_extratos["Data"] = pd.to_datetime(df_extratos["Data"], format="%d/%m/%y às %H:%M:%S")
# df_extratos.sort_values(by="Data", inplace=True)

# df_faturas["Data"] = pd.to_datetime(df_faturas["Data"], format="%d/%m/%Y")
# df_faturas.sort_values(by="Data", inplace=True)

# df_extratos.to_csv("extratos.csv", index=False, encoding="utf-8-sig")
# df_faturas.to_csv("faturas.csv", index=False, encoding="utf-8-sig")

# from services.pluggy.sync import sync

# sync()

# from services.pluggy.pluggy_client import listar_transacoes

# account_id = "2d0df1dd-e6d8-4f0a-8cc1-7aa62bdf6d25"
# t = listar_transacoes(account_id)
