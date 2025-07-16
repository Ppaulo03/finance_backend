from app.services.db import FinanceDB
from schemas import FinanceEntrySchema, Account
import pandas as pd

df = pd.read_csv("data/AllData.csv")

db = FinanceDB()
db.connect()
db.drop_tables()
db = FinanceDB()
db.connect()
for index, row in df.iterrows():
    entry = FinanceEntrySchema(**row)
    db.insert_financa(entry)

df = pd.read_csv(r"data\accounts.csv")
for index, row in df.iterrows():
    entry = Account(
        nome=row["nome"],
        saldo_inicial=row["saldo_inicial"],
    )
    db.insert_account(entry)
db.close()
