import yfinance as yf
import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import VAR
from arch import arch_model
from sklearn.linear_model import LinearRegression

def analisis_series(simbolo1, simbolo2="", modelo="ARIMA", periodo="6mo", mostrar_regresion=False):
    # Descarga de datos
    try:
        data1 = yf.download(simbolo1, period=periodo)
        if data1.empty:
            return f"Error: No se encontraron datos para {simbolo1}", None
        datos1 = data1['Close'].squeeze() # ver type de serie para estar seguro

        datos2 = None
        if simbolo2:
            data2 = yf.download(simbolo2, period=periodo)
            if not data2.empty:
                datos2 = data2['Close'].squeeze()
    except Exception as e:
        return f"Error en la descarga: {str(e)}", None

    # limpiar el proceso
    plt.clf()
    fig = plt.figure(figsize=(10, 5))
    
    #  regresión lineal si se selecciona 
    if mostrar_regresion and modelo != "VAR":
        X = np.arange(len(datos1)).reshape(-1, 1)
        y = datos1.values.reshape(-1, 1)
        lr_model = LinearRegression().fit(X, y)
        tendencia = lr_model.predict(X)
        plt.plot(datos1.index, tendencia, color='red', linestyle='--', label='Regresión lineal')
    
    if modelo == "ARIMA":
        # Modelo ARIMA uno
        arima_model = ARIMA(datos1, order=(1,1,1))
        arima_result = arima_model.fit()
        pred = arima_result.predict(start=0, end=len(datos1)-1)
        plt.plot(datos1, label=f"{simbolo1} Real")
        plt.plot(pred, color='orange', linestyle='--', label='ARIMA Ajuste')
        plt.title(f"ARIMA - {simbolo1}")
        plt.legend()
    
    elif modelo == "VAR":
        if datos2 is None:
            return "Para VAR debes ingresar un símbolo válido en Serie 2", None
        
        # Alinear fechas para VAR
        df = pd.concat([datos1, datos2], axis=1).dropna()
        df.columns = [simbolo1, simbolo2]
        
        var_model = VAR(df)
        var_result = var_model.fit(maxlags=5)
        pred = var_result.fittedvalues
        
        plt.plot(df[simbolo1], label=f"{simbolo1} Real")
        plt.plot(df[simbolo2], label=f"{simbolo2} Real")
        plt.plot(pred[simbolo1], linestyle='--', label=f'{simbolo1} Pred')
        plt.plot(pred[simbolo2], linestyle='--', label=f'{simbolo2} Pred')
        plt.title(f"VAR - {simbolo1} & {simbolo2}")
        plt.legend()
    
    elif modelo in ["ARCH", "GARCH"]:
        # Retornos log
        serie = 100 * datos1.pct_change().dropna()
        vol = 'Garch' if modelo == "GARCH" else 'ARCH'
        
        am = arch_model(serie, vol=vol, p=1, q=(1 if modelo == "GARCH" else 0))
        res = am.fit(disp="off")
        
        plt.plot(serie, label='Retornos %', alpha=0.5)
        plt.plot(res.conditional_volatility, color='red', label=f'Volatilidad {modelo}')
        plt.title(f"Análisis de Volatilidad {modelo} - {simbolo1}")
        plt.legend()
    
    plt.tight_layout()
    return f"Ejecución exitosa: {modelo}", fig

# Interfaz Gradio
iface = gr.Interface(
    fn=analisis_series,
    inputs=[
        gr.Textbox(label="Símbolo Serie 1 (ej: AAPL, BTC-USD)", value="AAPL"),
        gr.Textbox(label="Símbolo Serie 2 (Solo VAR, ej: MSFT)", value=""),
        gr.Dropdown(choices=["ARIMA", "VAR", "ARCH", "GARCH"], label="Modelo", value="ARIMA"),
        gr.Dropdown(choices=["1mo","3mo","6mo","1y","5y"], value="6mo", label="Periodo"),
        gr.Checkbox(label="Mostrar tendencia (Regresión Lineal)")
    ],
    outputs=[
        gr.Textbox(label="Estado"),
        gr.Plot(label="Visualización de Resultados")
    ],
    title="Dashboard de Series Temporales Financieras",
    description="Herramienta para el análisis técnico y estadístico de activos usando modelos econométricos."
)

iface.launch()
