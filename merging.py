## CODIGO DE CORRELACION ENTRE TABLAS
## ---------------------------------------
## PARAMETROS EJECUCION
date_start  = "2022-01-01"            #fecha de inicio
date_fin    = "2022-12-31"            #fecha de fin
manual_path = "data/manual.csv"       #ruta a archivo procesado pluvio manual
auto_path   = "data/automatico.csv"   #ruta a archivo procesado pluvio automatico
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
## ---------------------------------------

#########################################
###########   MERGING    ################
#########################################

# Recorriendo la tabla automatica en busca de coincidencias
cumulative_auto = []
auto_p = automatico.precip.to_list()
cum_m1 = []
for dmanual, duracion in zip(manual.fechahora, manual.duracion):
    idx0 = int(automatico[automatico.fechahora==dmanual].index[0])
    idxf = idx0 + duracion + 1 #+1 para contar a la hora inicial
    aux = auto_p[idx0:idxf+1]
    aux2 = auto_p[idx0-1:idxf+1]
    acum = np.sum(aux)
    cumulative_auto.append(acum)
    cum_m1.append(np.sum(aux2))

manual["acum"] = cumulative_auto #lluvia acumulada durante el evento
manual["acum_m1"] = cum_m1       #lluvia acumulada durante el evento + una hora antes


#########################################
###########   ANALISIS    ###############
#########################################
# Una vez con una tabla bien hecha, primero calculamos la diferencia entre
# la precip medida por el observador y la acumulada automaticamente

# Obtenemos la lista de observadores unicos
observers = manual.observador.unique()
print("Observadores en el rango dado")
#for i in observers: print(i)

# Calculamos ambas diferencias
pluviomanual = manual.pluvio.astype(float)
manual["d_pluv"] = pluviomanual - manual.acum
manual["d_pluv2"] = pluviomanual - manual.acum_m1

# Cantidad de eventos registrados por observador
bxdata = []; bxdata2 = []; names_wcount = []
for j in observers:
    aux = manual[manual.observador == j]
    print(j, len(aux))
    bxdata.append(aux.d_pluv)
    bxdata2.append(aux.d_pluv2)
    names_wcount.append(f"{j}-{len(aux)}")




fig, ax = plt.subplots(1,1)
ax.boxplot(bxdata)
ax.axhline(0, c = "k", lw = 0.5, alpha = .5)
ax.set_xticklabels(observers)
ax.set_ylabel("p_obs - p_auto")
ax.set_title(f"Diferencia entre medidas\n{date_start} al {date_fin}")



fig, ax2 = plt.subplots(1,1)
ax2.boxplot(bxdata2)
ax2.axhline(0, c = "k", lw = 0.5, alpha = .5)
ax2.set_xticklabels(names_wcount) #mostradno nombres con contador
#ax2.set_xticklabels(observers)    #mostrando solo nombres
ax2.set_ylabel("p_obs - p_auto")
ax2.set_title(f"Diferencia entre medidas + 1 hora\n{date_start} al {date_fin}")
plt.show()