from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from loguru import logger
import pandas as pd
import joblib


def carregar_dados(path: str):
    df = pd.read_csv(path)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Hora"] = df["Data"].dt.hour
    df["DiaSemana"] = df["Data"].dt.dayofweek
    df["Sinal"] = df["Valor"].apply(lambda x: 1 if x > 0 else 0)
    return df


def treinar_modelo(df: pd.DataFrame, target: str, features: list, save_path: str):
    df = df[features + [target]].dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        [
            ("tfidf_origem", TfidfVectorizer(), "Destino / Origem"),
            ("tfidf_desc", TfidfVectorizer(), "Descricao"),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        [
            ("preprocessador", preprocessor),
            ("modelo", RandomForestClassifier(random_state=42)),
        ]
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    report = classification_report(y_test, y_pred, zero_division=0)
    logs = f"\n=== Resultado para '{target}' ===\n{report}"
    with open("tagging/logs/training_log.txt", "a") as log_file:
        log_file.write(logs)

    joblib.dump(pipeline, save_path)
    logger.info(f"Modelo salvo em: {save_path}")


def train_models(df: pd.DataFrame):
    features = ["Valor", "Sinal", "Hora", "DiaSemana", "Destino / Origem", "Descricao"]
    targets = ["Tipo", "Categoria", "Subcategoria", "Nome"]

    with open("tagging/logs/training_log.txt", "w") as log_file:
        log_file.write("")

    for target in targets:
        caminho_modelo = f"tagging/models/modelo_{target.lower()}.pkl"
        treinar_modelo(df, target, features, caminho_modelo)


if __name__ == "__main__":
    caminho_csv = "data/AllData.csv"
    df = carregar_dados(caminho_csv)
    train_models(df)
