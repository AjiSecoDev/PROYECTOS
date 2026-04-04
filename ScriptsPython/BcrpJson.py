# Alternativa temporal para descargar los json del bcrp
# no se pueden descargar

import requests
import pandas as pd
import json
#url de ejemplo, cambiar
url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM/json"

# iniciamos
respuesta = requests.get(url)
contenido_html = respuesta.text

# extraemos los valores de pagina web, no se puede descargar
inicio = contenido_html.find("{")
fin = contenido_html.rfind("}") + 1
json_text = contenido_html[inicio:fin]

# modificar el JSON
data = json.loads(json_text)

# fechas y valores
periodos = [item["name"] for item in data["periods"]]
valores = [float(item["values"][0]) for item in data["periods"]]

# agrupamos
df = pd.DataFrame({
    "Fecha": periodos,
    "Valor": valores
})

# editamos las fechas de bcrp
meses = {
    "Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Ago": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"
}

def convertir_fecha(fecha):
    m, a = fecha.split(".")
    mes = meses[m]
    anio = a
    return pd.to_datetime(f"{anio}-{mes}-01")

df["Fecha"] = df["Fecha"].apply(convertir_fecha)

print(df.head(100))
