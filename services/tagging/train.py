from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from time import time
from loguru import logger
import pandas as pd
import joblib
import os

base_path = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = f"{base_path}/models"
LOG_PATH = f"{base_path}/logs"


def carregar_dados(path: str):
    df = pd.read_csv(path)
    df = df[df["need_tagging"] != True]
    df["Data"] = pd.to_datetime(df["Data"])
    df["Hora"] = df["Data"].dt.hour
    df["DiaSemana"] = df["Data"].dt.dayofweek
    df["Valor"] = df["Valor"].apply(lambda x: float(str(x).replace(",", ".")))
    df["Sinal"] = df["Valor"].apply(lambda x: 1 if x > 0 else 0)
    return df


def treinar_modelo(
    df: pd.DataFrame, target: str, features: list, save_path: str, time_marker: float
):
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
    with open(f"{LOG_PATH}/training_log_{time_marker}.txt", "a") as log_file:
        log_file.write(logs)

    joblib.dump(pipeline, save_path)
    logger.info(f"Modelo salvo em: {save_path}")


def train_models(caminho_csv: str):
    df = carregar_dados(caminho_csv)
    if len(df) < 20:
        return
    features = ["Valor", "Sinal", "Hora", "DiaSemana", "Destino / Origem", "Descricao"]
    targets = ["Tipo", "Categoria", "Subcategoria", "Nome"]

    os.makedirs(LOG_PATH, exist_ok=True)
    os.makedirs(MODEL_PATH, exist_ok=True)
    time_marker = time()
    for target in targets:
        caminho_modelo = f"{MODEL_PATH}/modelo_{target.lower()}.pkl"
        treinar_modelo(df, target, features, caminho_modelo, time_marker)
