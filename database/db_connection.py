import pymysql
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator
from loguru import logger


class MySQLConfig(BaseModel):
    host: str
    port: int
    password: str
    user: str
    database: Optional[str] = None

    @field_validator("port")
    def validate_host(cls, value: Any) -> int:
        return int(value)


class MySQLConnection:
    def __init__(
        self,
        user_id: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 3306,
        database: Optional[str] = None,
    ):
        self.config = MySQLConfig(
            host=host, port=port, user=user, password=password, database=database
        )
        self.user_id = user_id
        self.database = database
        self.conn: Optional[pymysql.Connection] = None

    def connect(self, create_db_if_missing=False):
        self.conn = pymysql.connect(**self.config.model_dump())
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

        campos.append("user_id")
        valores.append(f"{self.user_id}")
        placeholders = ", ".join(["%s"] * len(campos))
        colunas = ", ".join(campos)

        sql = f"INSERT INTO {table} ({colunas}) VALUES ({placeholders})"
        self.execute(sql, valores)

    def get_table(self, table: str) -> list[dict]:
        sql = f"SELECT * FROM {table} WHERE user_id='{self.user_id}'"
        results = self.fetchall(sql)
        if not results:
            logger.info(f"Nenhuma entrada encontrada na tabela {table}.")
            return []

        cleaned_results = []
        for row in results:
            cleaned_row = {
                key: value.strip() if isinstance(value, str) else value
                for key, value in row.items()
            }
            cleaned_results.append(cleaned_row)
        return cleaned_results

    def close(self):
        if self.conn:
            self.conn.close()
        self.conn = None
