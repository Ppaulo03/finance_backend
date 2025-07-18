from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class FinanceEntrySchema(BaseModel):
    id: int = Field(
        default=0, description="Unique identifier for the finance entry", alias="id"
    )
    data: datetime = Field(..., description="Date and time of the entry", alias="Data")
    valor: float = Field(..., description="Monetary value of the entry", alias="Valor")
    destino_origem: str = Field(
        ..., description="Destination or origin of the entry", alias="Destino / Origem"
    )
    descricao: str = Field(
        ..., description="Description of the entry", alias="Descricao"
    )
    tipo: str = Field(
        ..., description="Type of the entry (e.g., income, expense)", alias="Tipo"
    )
    categoria: str = Field(
        ...,
        description="Category of the entry (e.g., food, transport)",
        alias="Categoria",
    )
    subcategoria: str = Field(
        ...,
        description="Subcategory of the entry (e.g., groceries, fuel)",
        alias="Subcategoria",
    )
    nome: str = Field(..., description="Name associated with the entry", alias="Nome")
    conta: int = Field(
        ..., description="Account associated with the entry", alias="Conta"
    )
    notas: str = Field(
        default="", description="Additional notes for the entry", alias="Notas"
    )

    @field_validator("valor", mode="before")
    def parse_valor(cls, v):
        if isinstance(v, str):
            try:
                return float(v.replace(",", "."))  # permite números com vírgula
            except ValueError as e:
                raise ValueError(f"Não foi possível converter '{v}' para float.") from e
        return v


class Account(BaseModel):
    id: int = Field(default=0, description="Unique identifier for the account")
    nome: str = Field(..., description="Name of the account")
    saldo_inicial: float = Field(..., description="Current balance of the account")
    open_finance_id: str = Field(
        default="",
        description="Open Finance identifier for the account",
    )
