# PRIMER CUADRO PEA Y NO PEA

import pandas as pd

# OCUP300 y fa_ del csv 
cols_buscadas = lambda c: c == "OCUP300" or c.startswith("fa_")
df = pd.read_csv("Trim Dic-Ene-Feb26.csv", usecols=cols_buscadas)

# BUSCAMOS LA COLUMNA IN FA_
col_fa = [c for c in df.columns if c.startswith("fa_")][0]

# quitar espacio en blanco, convertir a numeros, 4 filas
v = df.assign(OCUP300=df["OCUP300"].str.strip(), 
              val=pd.to_numeric(df[col_fa], errors='coerce')) \
      .groupby("OCUP300")["val"].sum().reindex(["1","2","3","4"], fill_value=0)

# Totales + tabla final
pea, no_act, total = v["1"] + v["2"], v["3"] + v["4"], v.sum()
tabla_final = pd.DataFrame({
    "Condición": ["Población edad trabajar", "PEA", "  Ocupada", "  Desocupada", "No activa"],
    "Miles": [total/1e3, pea/1e3, v["1"]/1e3, v["2"]/1e3, no_act/1e3],
    "%": [100, (pea/total)*100, (v["1"]/pea)*100, (v["2"]/pea)*100, (no_act/total)*100]
}).round(1)

print(tabla_final)
