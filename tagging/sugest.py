# suggest.py
import pandas as pd
import joblib
from loguru import logger

MODEL_PATH = "tagging/models/"


def preparar_entrada(data, valor, origem, descricao):
    """Transforma os dados crus em um DataFrame com as features esperadas"""
    dt = pd.to_datetime(data)
    entrada = pd.DataFrame(
        [
            {
                "Data": dt,
                "Valor": valor,
                "Sinal": 1 if valor > 0 else 0,
                "Hora": dt.hour,
                "DiaSemana": dt.dayofweek,
                "Destino / Origem": origem,
                "Descricao": descricao,
            }
        ]
    )
    return entrada[
        ["Valor", "Sinal", "Hora", "DiaSemana", "Destino / Origem", "Descricao"]
    ]


def sugerir_rotulos(data, valor, origem, descricao, **kwargs):
    try:
        modelos = {
            "Tipo": joblib.load(f"{MODEL_PATH}modelo_tipo.pkl"),
            "Categoria": joblib.load(f"{MODEL_PATH}modelo_categoria.pkl"),
            "Subcategoria": joblib.load(f"{MODEL_PATH}modelo_subcategoria.pkl"),
            "Nome": joblib.load(f"{MODEL_PATH}modelo_nome.pkl"),
        }
    except FileNotFoundError as e:
        logger.warning(f"Erro ao carregar os modelos: {e}")
        return {}

    entrada = preparar_entrada(data, valor, origem, descricao)
    return {rotulo: modelo.predict(entrada)[0] for rotulo, modelo in modelos.items()}


if __name__ == "__main__":

    exemplo = {
        "data": "2025-07-08 00:00:00",
        "valor": -1500.00,
        "origem": "para conta investimento",
        "descricao": "Transferência enviada para conta investimento",
    }

    sugestao = sugerir_rotulos(**exemplo)
    logger.info("=== Sugestão de Rótulos ===")
    for k, v in sugestao.items():
        logger.info(f"{k}: {v}")
