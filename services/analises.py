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


def trend_analysis(df):

    df_gastos = df[df["tipo"] == "Gasto"].copy()
    df_gastos["valor"] = -df_gastos["valor"]
    # Garante que a data esteja como datetime
    df_gastos["data"] = pd.to_datetime(df_gastos["data"])

    # Garante que valores estejam negativos para gastos

    # Agrupa por mês e categoria
    df_gastos["mes"] = df_gastos["data"].dt.to_period("M").dt.to_timestamp()
    dados = df_gastos.groupby(["mes", "categoria"])["valor"].sum().unstack().fillna(0)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    dados.plot(ax=ax, marker="o")

    ax.set_title("Evolução dos Gastos por Categoria")
    ax.set_ylabel("Valor Gasto (R$)")
    ax.set_xlabel("Mês")
    ax.grid(True)
    ax.legend(title="Categoria", bbox_to_anchor=(1.05, 1), loc="upper left")
    fig.tight_layout()

    return fig


def tendencia_gastos_totais(df, janela_ma=True, meses_prever=1):
    # Garante datetime
    df["data"] = pd.to_datetime(df["data"])

    # Filtra apenas gastos (valores negativos)
    df_gastos = df[df["tipo"] == "Gasto"].copy()
    df_gastos["valor"] = -df_gastos["valor"]

    # Agrupa por mês
    df_gastos["mes"] = df_gastos["data"].dt.to_period("M").dt.to_timestamp()
    df_mes = df_gastos.groupby("mes")["valor"].sum().reset_index()

    # Calcula média móvel (opcional)
    if janela_ma:
        df_mes["media_movel"] = df_mes["valor"].rolling(window=3, min_periods=1).mean()
    else:
        df_mes["media_movel"] = df_mes["valor"]

    # Projeção simples: usa a média móvel dos últimos 3 meses para prever o próximo mês
    ultimo_mes = df_mes["mes"].max()
    prox_mes = ultimo_mes + pd.offsets.MonthBegin(1)
    projecao = (
        df_mes["media_movel"].iloc[-3:].mean()
        if len(df_mes) >= 3
        else df_mes["media_movel"].iloc[-1]
    )

    # Prepara dados para plotar projeção
    df_proj = pd.DataFrame(
        {"mes": [prox_mes], "valor": [projecao], "media_movel": [projecao]}
    )

    # Plotagem
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_mes["mes"], df_mes["valor"], marker="o", label="Gastos Mensais")
    ax.plot(
        df_mes["mes"],
        df_mes["media_movel"],
        linestyle="--",
        label="Média Móvel (3 meses)",
    )

    # Projeção (ponto separado, com cor diferente)
    ax.scatter(
        df_proj["mes"],
        df_proj["valor"],
        color="red",
        label="Projeção Próximo Mês",
        zorder=5,
    )
    ax.annotate(
        f"R$ {projecao:,.2f}",
        (df_proj["mes"].iloc[0], df_proj["valor"].iloc[0]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        color="red",
    )

    ax.set_title("Tendência dos Gastos Totais Mensais")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor Gasto (R$)")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    return fig


def gastos_recorrentes(df, min_meses=3):
    # Garante datetime
    df["data"] = pd.to_datetime(df["data"])

    # Considera apenas gastos (valores negativos)
    df_gastos = df[df["tipo"] == "Gasto"].copy()
    df_gastos["valor"] = -df_gastos["valor"]

    # Extrai mês (período)
    df_gastos["mes"] = df_gastos["data"].dt.to_period("M")

    # Conta em quantos meses diferentes cada nome apareceu
    frequencia_meses = (
        df_gastos.groupby(["nome"])["mes"]
        .nunique()
        .reset_index()
        .rename(columns={"mes": "meses_ativos"})
    )

    # Filtra só os que aparecem em pelo menos min_meses meses
    recorrentes = frequencia_meses[frequencia_meses["meses_ativos"] >= min_meses]

    # Calcula soma e média dos gastos para cada nome recorrente
    resumo = (
        df_gastos[df_gastos["nome"].isin(recorrentes["nome"])]
        .groupby("nome")["valor"]
        .agg(["sum", "mean", "count"])
        .reset_index()
    )

    # Junta com meses_ativos
    resumo = resumo.merge(recorrentes, on="nome")

    # Ordena pelo gasto total decrescente
    resumo = resumo.sort_values(by="sum", ascending=False)

    # Renomeia colunas para apresentação
    resumo = resumo.rename(
        columns={
            "nome": "Nome",
            "sum": "Gasto Total (R$)",
            "mean": "Gasto Médio por Ocorrência (R$)",
            "count": "Ocorrências",
            "meses_ativos": "Meses Ativos",
        }
    )

    return resumo
