from .db_connection import MySQLConnection
from schemas import FinanceEntrySchema, Account

import pandas as pd

USER = "root"
PASSWORD = "0123"
DATABASE = "financeiro"


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
        print("Tabelas removidas com sucesso.")

    def insert_financa(self, entry: "FinanceEntrySchema"):
        self.insert(entry, "financas")
        print("Entrada financeira inserida com sucesso.")

    def insert_account(self, account: "Account"):
        self.insert(account, "contas")
        print("Conta inserida com sucesso.")

    def get_financas(self) -> pd.DataFrame:
        return self.get_table("financas")

    def get_accounts(self) -> pd.DataFrame:
        return self.get_table("contas")
