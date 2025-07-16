import MySQLdb
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List, Dict, Any
from loguru import logger


class MySQLConnection:
    def __init__(self, user, password, host="localhost", database=None):
        self.config = {
            "user": user,
            "passwd": password,
            "host": host,
        }
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self, create_db_if_missing=False):
        # Conecta sem o banco especificado (para criar, se necessário)
        self.conn = MySQLdb.connect(**self.config)
        self.cursor = self.conn.cursor()

        if create_db_if_missing and self.database:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

        self.cursor.close()
        self.conn.close()

        # Conecta ao banco especificado
        self.conn = MySQLdb.connect(**self.config, db=self.database)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetchall(self, query, params=None) -> List[Dict[str, Any]]:
        self.cursor.execute(query, params or ())
        results = self.cursor.fetchall()
        return [
            {col[0]: row[i] for i, col in enumerate(self.cursor.description)}
            for row in results
        ]

    def fetchone(self, query, params=None) -> Optional[Dict[str, Any]]:
        self.cursor.execute(query, params or ())
        result = self.cursor.fetchone()
        return (
            {col[0]: result[i] for i, col in enumerate(self.cursor.description)}
            if result
            else None
        )

    def insert(self, entry: "BaseModel", table: str):
        campos = [field for field in entry.model_fields_set if field != "id"]
        valores = [getattr(entry, campo) for campo in campos]

        placeholders = ", ".join(["%s"] * len(campos))
        colunas = ", ".join(campos)

        sql = f"INSERT INTO {table} ({colunas}) VALUES ({placeholders})"
        self.execute(sql, valores)

    def get_table(self, table: str) -> pd.DataFrame:
        self.connect()
        sql = f"SELECT * FROM {table}"
        results = self.fetchall(sql)
        df = pd.DataFrame(results)
        self.close()
        if df.empty:
            logger.info(f"Nenhuma entrada encontrada na tabela {table}.")
            return pd.DataFrame()

        return df

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
