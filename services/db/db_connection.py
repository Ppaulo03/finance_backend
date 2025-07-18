import MySQLdb
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List, Dict, Any
from loguru import logger


class MySQLConnection:
    def __init__(self, user, password, host="localhost", port=3306, database=None):
        self.config = {
            "host": host,
            "port": int(port),
            "user": user,
            "passwd": password,
        }
        self.database = database
        self.conn = None

    def connect(self, create_db_if_missing=False):

        self.conn = MySQLdb.connect(**self.config)

        with self.conn.cursor() as cursor:
            if create_db_if_missing and self.database:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            if self.database:
                cursor.execute(f"USE {self.database}")

    def execute(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params or ())
        self.conn.commit()

    def fetchall(self, query, params=None) -> List[Dict[str, Any]]:
        with self.conn.cursor() as cursor:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return [
                {col[0]: row[i] for i, col in enumerate(cursor.description)}
                for row in results
            ]

    def fetchone(self, query, params=None) -> Optional[Dict[str, Any]]:
        with self.conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return (
                {col[0]: result[i] for i, col in enumerate(cursor.description)}
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
        sql = f"SELECT * FROM {table}"
        results = self.fetchall(sql)
        df = pd.DataFrame(results)

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.strip() if df[col].dtype == "object" else df[col]

        if df.empty:
            logger.info(f"Nenhuma entrada encontrada na tabela {table}.")
            return pd.DataFrame()

        return df

    def close(self):

        if self.conn:
            self.conn.close()

        self.conn = None
