## CODIGO DE CORRELACION ENTRE TABLAS
## ---------------------------------------
## PARAMETROS EJECUCION
date_start  = "2023-01-01"            #fecha de inicio
date_fin    = "2023-12-31"            #fecha de fin
manual_path = "data/manual.csv"       #ruta a archivo procesado pluvio manual
auto_path   = "data/automatico.csv"   #ruta a archivo procesado pluvio automatico
## ---------------------------------------

# Librerias
import pandas as pd
import datetime as dt
import numpy as np

# Leyendo archivos
manual = pd.read_csv(manual_path)
automatico = pd.read_csv(auto_path)
manual["fechahora"] = pd.to_datetime(manual.fechahora)
automatico["fechahora"] = pd.to_datetime(automatico.fechahora)


# Recortando ambas tablas
d0 = dt.datetime.strptime(date_start, "%Y-%m-%d")
df = dt.datetime.strptime(date_fin, "%Y-%m-%d")
manual = manual.loc[(manual.fechahora > d0) & (manual.fechahora < df)]
automatico = automatico.loc[(automatico.fechahora > d0) & (automatico.fechahora < df)]
automatico.reset_index(inplace = True)

# MERGING
# Recorriendo la tabla automatica en busca de coincidencias
cumulative_auto = []
"""
for dmanual, duracion in zip(manual.fechahora, manual.duracion):
    dfmanual = dmanual + dt.timedelta(hours = duracion)
    aux = automatico.loc[(automatico.fechahora >= dmanual) & (automatico.fechahora <= dfmanual)]
    acum = np.sum(aux.precip)
    cumulative_auto.append(acum)
"""
auto_p = automatico.precip.to_list()
for dmanual, duracion in zip(manual.fechahora, manual.duracion):
    idx0 = int(automatico[automatico.fechahora==dmanual].index[0])
    idxf = idx0 + duracion + 1 #+1 para contar a la hora inicial
    aux = auto_p[idx0:idxf+1]
    acum = np.sum(aux)
    cumulative_auto.append(acum)

manual["acum"] = cumulative_auto
print(manual.head())
