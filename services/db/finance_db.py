from .db_connection import MySQLConnection
from schemas import FinanceEntrySchema, Account
from services.tagging import train_models

from time import time
from os import getenv
from dotenv import load_dotenv
from loguru import logger
import pandas as pd

load_dotenv(override=True)
HOST = getenv("MYSQL_HOST")
PORT = getenv("MYSQL_PORT")
USER = getenv("MYSQL_USER")
PASSWORD = getenv("MYSQL_PASSWORD")
DATABASE = "financeiro"

backup_folder = "data/backup"
db_file = "data/AllData.csv"


class FinanceDB(MySQLConnection):
    def __init__(
        self, user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE
    ):
        super().__init__(
            user=user, password=password, host=host, port=port, database=database
        )

        self.connect(create_db_if_missing=True)
        self.create_tables()

    def create_tables(self):
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
                notas TEXT,
                need_tagging BOOLEAN DEFAULT FALSE
            )
        """
        )

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS contas(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                saldo_inicial FLOAT NOT NULL,
                open_finance_id VARCHAR(100) NOT NULL,
                is_credit BOOLEAN DEFAULT FALSE
            )
            """
        )

    def drop_tables(self):
        self.execute("DROP TABLE IF EXISTS financas")
        self.execute("DROP TABLE IF EXISTS contas")

    def reset_tables(self):
        self.drop_tables()
        self.create_tables()

    def insert_financa(self, entry: "FinanceEntrySchema"):
        self.insert(entry, "financas")

    def insert_account(self, account: "Account"):
        self.insert(account, "contas")

    def get_financas(self) -> pd.DataFrame:
        return self.get_table("financas")

    def get_accounts(self) -> pd.DataFrame:
        return self.get_table("contas")

    def add_df_entries(self, entries_df: pd.DataFrame):
        entries_df.drop(columns=["id"], inplace=True, errors="ignore")

        for _, row in entries_df.iterrows():
            entry = FinanceEntrySchema(**row)
            self.insert_financa(entry)

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

    def get_treated_data(self) -> pd.DataFrame:
        """Retorna os dados tratados do banco de dados."""
        df = self.get_financas()
        if df.empty:
            logger.warning("Nenhum dado encontrado na tabela 'financas'.")
            return pd.DataFrame()

        df["data"] = pd.to_datetime(df["data"])
        df["valor"] = df["valor"].astype(float)
        df["conta"] = df["conta"].astype(int)

        # Renomeia colunas para padronização
        df.rename(
            columns={
                "destino_origem": "Destino / Origem",
                "descricao": "Descrição",
                "tipo": "Tipo",
                "categoria": "Categoria",
                "subcategoria": "Subcategoria",
                "nome": "Nome",
            },
            inplace=True,
        )
        return df
