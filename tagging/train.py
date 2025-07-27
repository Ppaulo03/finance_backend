import joblib, os
from loguru import logger

from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
from scipy.sparse import csr_matrix
from csv import reader
from datetime import datetime
import numpy as np


def load_data(caminho_csv: str) -> list[dict]:
    data = []
    targets_columns = ["tipo", "categoria", "subcategoria", "nome"]
    with open(caminho_csv, "r", encoding="utf-8-sig") as f:
        csv_linhas = reader(f, delimiter=",")
        headers = next(csv_linhas)
        for linha in csv_linhas:
            line = dict(zip(headers, linha))
            print(line)
            line["need_tagging"] = line["need_tagging"] == "True"
            if not bool(line.get("need_tagging")):
                line["data"] = datetime.strptime(line["data"], "%Y-%m-%dT%H:%M:%S")

                features = [
                    float(line["valor"]),
                    line["descricao"].strip(),
                    line["destino_origem"].strip(),
                    line["data"].month,
                    line["data"].weekday(),
                    line["data"].hour,
                ]

                target = []
                for col in targets_columns:
                    target.append(line[col].strip())

                data.append({"features": features, "target": target})
    return data


def train_models(caminho_csv: str):

    data = load_data(caminho_csv)

    X = [d["features"] for d in data]
    y = [d["target"] for d in data]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Criar os vetorizadores e scaler separadamente
    scaler_valor = StandardScaler()
    tfidf_descricao = TfidfVectorizer()
    tfidf_destino_origem = TfidfVectorizer()

    valor_train = []
    descricao_train = []
    destino_origem_train = []
    for x in X_train:
        valor_train.append(x[0])
        descricao_train.append(x[1])
        destino_origem_train.append(x[2])
    valor_train = np.array(valor_train).reshape(-1, 1)

    scaler_valor.fit(valor_train)
    tfidf_descricao.fit(descricao_train)
    tfidf_destino_origem.fit(destino_origem_train)

    valor_scaled = scaler_valor.transform(valor_train)
    desc_vect = tfidf_descricao.transform(descricao_train)
    dest_vect = tfidf_destino_origem.transform(destino_origem_train)

    extras = [[x[3], x[4], x[5]] for x in X_train]
    extras_sparse = csr_matrix(extras)

    X_train_final = hstack([valor_scaled, desc_vect, dest_vect, extras_sparse])

    # Treinar o modelo
    clf = MultiOutputClassifier(
        RandomForestClassifier(n_estimators=100, random_state=42)
    )
    clf.fit(X_train_final, y_train)

    valor_test = []
    descricao_test = []
    destino_origem_test = []
    for x in X_test:
        valor_test.append(x[0])
        descricao_test.append(x[1])
        destino_origem_test.append(x[2])
    valor_test = np.array(valor_test).reshape(-1, 1)

    valor_scaled_test = scaler_valor.transform(valor_test)
    desc_vect_test = tfidf_descricao.transform(descricao_test)
    dest_vect_test = tfidf_destino_origem.transform(destino_origem_test)
    extras = [[x[3], x[4], x[5]] for x in X_test]
    extras_test = csr_matrix(extras)

    X_test_final = hstack(
        [valor_scaled_test, desc_vect_test, dest_vect_test, extras_test]
    )

    y_test = np.array(y_test)
    acc = clf.score(X_test_final, y_test)
    logger.info(f"Acurácia média nas saídas: {acc:.2f}")

    base_path = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_path, "models")
    os.makedirs(model_dir, exist_ok=True)

    # Salvar artefatos
    joblib.dump(clf, os.path.join(model_dir, "tag_model.joblib"))
    joblib.dump(tfidf_descricao, os.path.join(model_dir, "tfidf_descricao.joblib"))
    joblib.dump(
        tfidf_destino_origem, os.path.join(model_dir, "tfidf_destino_origem.joblib")
    )
    joblib.dump(scaler_valor, os.path.join(model_dir, "scaler_valor.joblib"))

    logger.info(f"Modelos e transformadores salvos em {model_dir}")


if __name__ == "__main__":
    train_models(r"C:\Users\Pichau\Documents\finance_backend\data\financas.csv")
