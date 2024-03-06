## CODIGO DE CORRELACION ENTRE TABLAS
## ---------------------------------------
## PARAMETROS EJECUCION
date_start  = "2023-01-01"            #fecha de inicio
date_fin    = "2023-12-31"            #fecha de fin
manual_path = "data/manual.csv"       #ruta a archivo procesado pluvio manual
auto_path   = "data/automatico.csv"   #ruta a archivo procesado pluvio automatico
threshold   = 1                       #cantidad de eventos para tomar en cuenta un observador
## ---------------------------------------

# Librerias
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
## ---------------------------------------

#########################################
###########   PROCESANDO   ##############
#########################################


# Leyendo archivos
manual = pd.read_csv(manual_path)
automatico = pd.read_csv(auto_path)
manual["fechahora"] = pd.to_datetime(manual.fechahora)
automatico["fechahora"] = pd.to_datetime(automatico.fechahora)
## ---------------------------------------


# Recortando ambas tablas
d0 = dt.datetime.strptime(date_start, "%Y-%m-%d")
df = dt.datetime.strptime(date_fin, "%Y-%m-%d")
manual = manual.loc[(manual.fechahora > d0) & (manual.fechahora < df)]
automatico = automatico.loc[(automatico.fechahora > d0) & (automatico.fechahora < df)]
automatico.reset_index(inplace = True)
automatico = automatico.iloc[:,1:]

# Obteniendo los datos del automatico que no fueron registrados, primero quitando
# los datos
def create_dts(start, duration):
    dts = []
    for i in range(duration+1):
        dd = start + dt.timedelta(hours=i)
        dts.append(dd)

    return dts


#def evento(idx0, idxf):


autom = automatico.copy()
    
for dmanual, duracion in zip(manual.fechahora, manual.duracion):
    lst = create_dts(dmanual, duracion)
    for i in lst:
        autom = autom[autom.fechahora != i]
    
autom.reset_index(inplace = True)
autom = autom.iloc[:,1:]
#autom.to_csv("prueba.csv")
print(autom.head())
p = autom.precip.to_list()
for i in range(len(p)):
    if p[i] > 0:
        idx0 = i
        u = i
        while p[u] != 0:
            u = u + 1
        idxf = u
        i = u

