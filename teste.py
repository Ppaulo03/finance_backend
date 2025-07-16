# from database import FinanceDB
# from schemas import FinanceEntrySchema, Account
# import pandas as pd

# df = pd.read_csv("data/AllData.csv")

# db = FinanceDB()
# db.connect()

# for index, row in df.iterrows():
#     entry = FinanceEntrySchema(
#         data=row["Data"],
#         valor=row["Valor"],
#         destino_origem=row["Destino / Origem"],
#         descricao=row["Descricao"],
#         tipo=row["Tipo"],
#         categoria=row["Categoria"],
#         subcategoria=row["Subcategoria"],
#         nome=row["Nome"],
#         conta=row["Conta"],
#         notas=row["Notas"],
#     )
#     db.insert_financa(entry)

# df = pd.read_csv(r"database\files\accounts.csv")
# for index, row in df.iterrows():
#     entry = Account(
#         nome=row["nome"],
#         saldo_inicial=row["saldo_inicial"],
#     )
#     db.insert_account(entry)
# db.close()


from pydantic import BaseModel, Field
import pandas as pd


class TesteSchema(BaseModel):
    id: int = Field(
        default=0, description="Unique identifier for the test entry", alias="id"
    )
    name: str = Field(..., description="Name of the test entry", alias="Nome")
    value: float = Field(
        ..., description="Value associated with the test entry", alias="Valor"
    )


teste = TesteSchema(Nome="Teste", Valor=123.45)
print(teste.model_dump())
print(teste.model_dump(by_alias=True))

df = pd.DataFrame([teste.model_dump()])
print(df)
