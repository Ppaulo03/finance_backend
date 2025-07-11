from pydantic import BaseModel, Field
from datetime import datetime


class FinanceEntrySchema(BaseModel):
    id: int = Field(default=0, description="Unique identifier for the finance entry")
    data: datetime = Field(..., description="Date and time of the entry")
    valor: float = Field(..., description="Monetary value of the entry")
    destino_origem: str = Field(..., description="Destination or origin of the entry")
    descricao: str = Field(..., description="Description of the entry")
    tipo: str = Field(..., description="Type of the entry (e.g., income, expense)")
    categoria: str = Field(
        ..., description="Category of the entry (e.g., food, transport)"
    )
    subcategoria: str = Field(
        ..., description="Subcategory of the entry (e.g., groceries, fuel)"
    )
    nome: str = Field(..., description="Name associated with the entry")
    conta: int = Field(..., description="Account associated with the entry")
    notas: str = Field(..., description="Additional notes for the entry")


class Account(BaseModel):
    id: int = Field(default=0, description="Unique identifier for the account")
    nome: str = Field(..., description="Name of the account")
    saldo_inicial: float = Field(..., description="Current balance of the account")
