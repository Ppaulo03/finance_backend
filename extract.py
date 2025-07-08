import pandas as pd
import json


def clean_money_value(value: str) -> float:
    """Limpa e converte valores monetários para float."""
    return float(
        value.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "")
    )


def classificar_operacao(row: pd.Series) -> str:
    """Classifica o tipo de operação com base na descrição e valor."""
    if row["Descricao"].startswith("Transferência"):
        return "Transferência"
    return "Gasto" if row["Valor"] < 0 else "Recebimento"


def extract_extrato(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai e transforma os dados do extrato bancário."""
    df = df.drop(columns=["Saldo"], errors="ignore")
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%y às %H:%M:%S")
    df["Valor"] = df["Valor"].apply(clean_money_value)
    df["Operacao"] = df.apply(classificar_operacao, axis=1)
    df["Destino / Origem"] = df["Descricao"].str.extract(
        r"(?:para|de|da)\s+(.+)", expand=False
    )
    df["Destino / Origem"] = df["Destino / Origem"].fillna(df["Descricao"])
    df["Destino / Origem"] = df["Destino / Origem"].fillna("")
    return df


def extract_fatura(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai e transforma os dados da fatura do cartão de crédito."""
    df = df.drop(columns=["Portador", "Parcela"], errors="ignore")
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
    df["Valor"] = df["Valor"].apply(clean_money_value)
    df["Valor"] = -df["Valor"]
    df["Descricao"] = "Compra no Cartão de Crédito"
    df["Operacao"] = df.apply(classificar_operacao, axis=1)
    df = df.rename(columns={"Estabelecimento": "Destino / Origem"})
    return df


def extract_data(file_path: str) -> pd.DataFrame:
    """Carrega os dados de um arquivo CSV e retorna um DataFrame."""
    df = pd.read_csv(file_path, delimiter=";")
    df = extract_extrato(df) if "Saldo" in df.columns else extract_fatura(df)


    df.rename(
        columns={
            "Operacao": "Tipo",
        },
        inplace=True,
    )
    return df[["Data", "Valor", "Destino / Origem", "Descricao", "Tipo"]]


def extract_bulk_data(file_paths: list) -> pd.DataFrame:
    """Extrai dados de múltiplos arquivos CSV e concatena em um único DataFrame."""
    dataframes = [extract_data(file_path) for file_path in file_paths]
    return pd.concat(dataframes, ignore_index=True)


if __name__ == "__main__":
    import os

    file_paths = os.listdir("raw_data")
    file_paths = [
        os.path.join("raw_data", file) for file in file_paths if file.endswith(".csv")
    ]
    df = extract_bulk_data(file_paths)
    df = df.drop_duplicates()
    df.to_csv("extrato_final.csv", index=False, encoding="utf-8-sig", sep=";")
