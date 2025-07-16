from .db_connection import MySQLConnection
from schemas import FinanceEntrySchema, Account
from services.tagging import train_models
from loguru import logger
from time import time
import pandas as pd

USER = "root"
PASSWORD = "0123"
DATABASE = "financeiro"

backup_folder = "data/backup"
db_file = "data/AllData.csv"


class FinanceDB(MySQLConnection):
    def __init__(self, user=USER, password=PASSWORD, database=DATABASE):
        super().__init__(user=user, password=password, database=database)

        self.connect(create_db_if_missing=True)
        self.execute(
            """
                    CREATE TABLE IF NOT EXISTS financas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        data DATETIME NOT NULL,
                        valor FLOAT NOT NULL,
                        destino_origem VARCHAR(255) NOT NULL,
                        descricao TEXT NOT NULL,
                        tipo VARCHAR(50) NOT NULL,
                        categoria VARCHAR(100) NOT NULL,
                        subcategoria VARCHAR(100) NOT NULL,
                        nome VARCHAR(255) NOT NULL,
                        conta INT NOT NULL,
                        notas TEXT
                    )
                """
        )

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS contas(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                saldo_inicial FLOAT NOT NULL
            )
            """
        )

        self.close()

    def drop_tables(self):
        self.connect()
        self.execute("DROP TABLE IF EXISTS financas")
        self.execute("DROP TABLE IF EXISTS contas")
        self.close()
        logger.info("Tabelas removidas com sucesso.")

    def insert_financa(self, entry: "FinanceEntrySchema"):
        self.insert(entry, "financas")
        logger.info("Entrada financeira inserida com sucesso.")

    def insert_account(self, account: "Account"):
        self.insert(account, "contas")
        logger.info("Conta inserida com sucesso.")

    def get_financas(self) -> pd.DataFrame:
        return self.get_table("financas")

    def get_accounts(self) -> pd.DataFrame:
        return self.get_table("contas")

    def add_df_entries(self, entries_df: pd.DataFrame):
        entries_df.drop(columns=["id"], inplace=True, errors="ignore")
        self.connect()

        for _, row in entries_df.iterrows():
            entry = FinanceEntrySchema(**row)
            self.insert_financa(entry)
        self.close()

        entries_df.to_csv(
            f"{backup_folder}/entries/entry_{int(time())}.csv",
            index=False,
            encoding="utf-8-sig",
        )

        all_df = pd.read_csv(db_file, encoding="utf-8-sig")
        all_df = pd.concat([all_df, entries_df], ignore_index=True)
        all_df.to_csv(db_file, index=False, encoding="utf-8-sig")
        all_df.to_csv(
            f"{backup_folder}/all_data/AllData_{int(time())}.csv",
            index=False,
            encoding="utf-8-sig",
        )
        train_models(db_file)
