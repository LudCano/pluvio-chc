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

obs_data = pd.read_csv("outputs/observador_por_dia.csv")
obs_d = pd.to_datetime(obs_data.fecha)
obs_data["fecha_"] = [i.date() for i in obs_d]
# recortando el df para hacer rápida la búsqueda
def buscar_obser(fecha):
    m = obs_data[obs_data.fecha_ == fecha]
    obs = m.observador.to_list()[0]
    return obs

autom = automatico.copy()
    
for dmanual, duracion in zip(manual.fechahora, manual.duracion):
    lst = create_dts(dmanual, duracion)
    for i in lst:
        autom = autom[autom.fechahora != i]
    
autom.reset_index(inplace = True)
autom = autom.iloc[:,1:]
autom.to_csv("prueba.csv")
#print(autom.head())
p = autom.precip.to_list()
dateti = autom.fechahora.to_list()
i = 0
## OBTENIENDO INDICES DE EVENTOS QUE TIENEN PRECIP >0
# obtenemos solamente los indices inicial y final, luego recortaremos
acum_lost = []; duraciones = []; hora_ini = []; observador_lost = []
while i <= len(p)-1:
    if p[i] > 0:
        idx0 = i
        ac = p[i] #creado acumulado de la primera hora
        u = i
        while p[u] != 0:
            u = u + 1
            ac = ac + p[u] # se suma a las horas de este evento
        idxf = u
        i = u
        acum_lost.append(round(ac,1)) #acumulado sumado
        duraciones.append(idxf-idx0) #NOTA: Duración es horas después de la hora inicial
        hora_ini.append(dateti[idx0])
        f = dateti[idx0].date()
        o = buscar_obser(f)
        observador_lost.append(o)
    else:
        i = i+1

df2 = pd.DataFrame(list(zip(hora_ini, duraciones, acum_lost, observador_lost)), columns = ["fechahora", "duracion", "precip", "observador"])
df2.to_csv("outputs/eventos_perdidos.csv", index = False)