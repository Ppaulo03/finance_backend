import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def gastos_por_categoria(df: pd.DataFrame):
    df_gastos = df[df["tipo"] == "Gasto"].copy()
    agrupado = df_gastos.groupby("categoria")["valor"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=agrupado.index, x=-agrupado.values, ax=ax)
    ax.set_xlabel("Total Gasto (R$)")
    ax.set_ylabel("Categoria")
    return fig


def gastos_por_semana(df: pd.DataFrame):
    df_gastos = df[df["tipo"] == "Gasto"].copy()
    df_gastos["semana"] = df_gastos["data"].dt.to_period("W").dt.start_time
    df_gastos["valor"] = -df_gastos["valor"]
    semana = df_gastos.groupby("semana")["valor"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=semana, x="semana", y="valor", marker="o", ax=ax)
    ax.set_ylabel("Gasto Total (R$)")
    ax.tick_params(rotation=30)
    return fig, semana


def pizza_gastos_por_categoria(df):
    df_gastos = df[df["tipo"] == "Gasto"].copy()
    df_gastos["valor"] = -df_gastos["valor"]
    dados = df_gastos.groupby("categoria")["valor"].sum().sort_values(ascending=False)

    limite = 7
    if len(dados) > limite:
        outros = dados[limite:].sum()
        dados = dados[:limite]
        if "Outros" not in dados.index:
            dados = dados.append(pd.Series({"Outros": outros}))
        else:
            dados["Outros"] += outros
    dados = dados.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(3, 3))
    wedges, texts, autotexts = ax.pie(
        dados,
        labels=dados.index,
        autopct="%.1f%%",
        startangle=90,
        textprops={"fontsize": 6},
    )

    ax.axis("equal")
    ax.tick_params(rotation=30)
    ax.set_title("Distribuição de Gastos por Categoria", fontsize=12)
    fig.tight_layout()
    return fig


def comparativo_gasto_receita(df):

    proporcao = df.groupby("tipo")["valor"].sum()
    proporcao = proporcao.reindex(["Recebimento", "Gasto"], fill_value=0)
    proporcao["Gasto"] = -proporcao.get("Gasto", 0)

    fig, ax = plt.subplots(figsize=(3, 3))
    proporcao.plot.pie(
        ax=ax,
        autopct="%.1f%%",
        startangle=90,
        colors=["#2ecc71", "#e74c3c"],
        labels=["Receitas", "Despesas"],
        textprops={"fontsize": 10},
    )
    ax.set_ylabel("")
    ax.set_title("Distribuição Total de Valores", fontsize=12)
    plt.tight_layout()
    return fig
