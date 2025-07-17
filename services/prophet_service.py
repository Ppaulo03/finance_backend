from prophet import Prophet
import plotly.graph_objects as go
import pandas as pd


def prever_gastos(df_semanais: pd.DataFrame, semanas=3):
    model = Prophet()
    df = df_semanais.rename(columns={"semana": "ds", "valor": "y"})
    model.fit(df)

    future = model.make_future_dataframe(periods=semanas, freq="W")
    forecast = model.predict(future)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["ds"], y=df["y"], name="Gasto Real"))
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"], y=forecast["yhat"], name="Previsão", line=dict(dash="dot")
        )
    )
    return fig, forecast
