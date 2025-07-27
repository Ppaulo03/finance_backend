import joblib, os
import json
from datetime import datetime
from scipy.sparse import hstack
from scipy.sparse import csr_matrix


base_path = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_path, "models")

# Carrega modelos e vocabulários
clf = joblib.load(os.path.join(model_dir, "tag_model.joblib"))
tfidf_descricao = joblib.load(os.path.join(model_dir, "tfidf_descricao.joblib"))
tfidf_destino_origem = joblib.load(
    os.path.join(model_dir, "tfidf_destino_origem.joblib")
)
scaler_valor = joblib.load(os.path.join(model_dir, "scaler_valor.joblib"))


def preprocess(raw):
    valor_scaled = scaler_valor.transform([[raw["valor"]]])
    desc_vect = tfidf_descricao.transform([raw["descricao"]])
    dest_vect = tfidf_destino_origem.transform([raw["destino_origem"]])
    dt = datetime.strptime(raw["data"], "%Y-%m-%dT%H:%M:%S")
    extras = csr_matrix([[dt.month, dt.weekday(), dt.hour]])
    X_input = hstack([csr_matrix(valor_scaled), desc_vect, dest_vect, extras])
    return X_input


def predict(entry):
    X = preprocess(entry)
    pred = clf.predict(X)
    return {
        "tipo": str(pred[0][0]),
        "categoria": str(pred[0][1]),
        "subcategoria": str(pred[0][2]),
        "nome": str(pred[0][3]),
    }
