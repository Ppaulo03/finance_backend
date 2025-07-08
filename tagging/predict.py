import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Carregue os dados rotulados
df = pd.read_csv("extrato_final - completo.csv")

# Combinar campos de entrada em um único texto para representar a transação
df["input_text"] = (
    df[["Valor", "Destino / Origem", "Descricao"]].astype(str).agg(" ".join, axis=1)
)

# Criar vetor TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["input_text"])

# Modelo de similaridade
nn = NearestNeighbors(n_neighbors=1, metric="cosine")
nn.fit(X)

# Nova entrada a ser classificada
entrada = "-83.9 RIOTGAME Compra no Cartão de Crédito"
entrada_vector = vectorizer.transform([entrada])
# Encontrar a transação mais parecida
_, indices = nn.kneighbors(entrada_vector)
transacao_similar = df.iloc[indices[0][0]]

# Mostrar sugestão
print("Sugestão de preenchimento:")
print("Tipo:", transacao_similar["Tipo"])
print("Categoria:", transacao_similar["Categoria"])
print("Subcategoria:", transacao_similar["Subcategoria"])
print("Nome:", transacao_similar["Nome"])
