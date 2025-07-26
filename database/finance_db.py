from .db_connection import MySQLConnection
from .finance_schema import FinanceEntrySchema, AccountSchema
from typing import List
from os import getenv
from dotenv import load_dotenv
from collections import Counter


load_dotenv(override=True)
HOST = getenv("MYSQL_HOST")
PORT = int(getenv("MYSQL_PORT"))
USER = getenv("MYSQL_USER")
PASSWORD = getenv("MYSQL_PASSWORD")
DATABASE = getenv("MYSQL_DATABASE")


class FinanceDB(MySQLConnection):
    def __init__(
        self,
        usuario_id: str,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE,
    ):
        super().__init__(
            user_id=usuario_id,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        self.connect(create_db_if_missing=True)
        self.create_tables()

    def create_tables(self):
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS financas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
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
                user_id VARCHAR(255) NOT NULL,
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

    def insert_account(self, account: "AccountSchema"):
        self.insert(account, "contas")

    def get_financas(self) -> List[FinanceEntrySchema]:
        finance_list = self.get_table("financas")
        return [FinanceEntrySchema(**entry) for entry in finance_list]

    def get_accounts(self) -> List[AccountSchema]:
        account_list = self.get_table("contas")
        return [AccountSchema(**account) for account in account_list]

    def add_entries(self, entries: List[FinanceEntrySchema]):
        finances = self.get_financas()

        def entry_key(entry):
            return (entry.data, entry.valor, entry.descricao, entry.destino_origem)

        entries.sort(key=lambda x: x.data)
        min_data = entries[0].data

        finances_filtered = [item for item in finances if item.data >= min_data]
        existing_counts = Counter(entry_key(item) for item in finances_filtered)

        new_counts = Counter(entry_key(entry) for entry in entries)
        inserted_counts = Counter()
        for entry in entries:
            key = entry_key(entry)
            # print(inserted_counts[key] + existing_counts.get(key, 0), new_counts[key])
            if inserted_counts[key] + existing_counts.get(key, 0) < new_counts[key]:
                print(entry)
                # self.insert_financa(entry)
                inserted_counts[key] += 1
