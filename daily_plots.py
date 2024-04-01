# ARCHIVOS DIARIOS

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import calendar
import scienceplots
plt.style.use(["science", "nature"])
## TIPOS DE EVENTO (columna "tipo")
## Tipo 0: Evento marcado manualmente (encontrado en pluvio manual)
## Tipo 1: Evento perdido (encontrado en pluvio automatico pero no manual)
## Tipo 2: No precipitado (ni en manual ni en automatico)

plot_boxes = True
plot_daily = False
threshold = True
d = pd.read_csv("outputs/daily_acum.csv")
d["fecha"] = pd.to_datetime(d.dia)

def gen_idx(l, n, g):
    idx0 = 0
    pars = []
    for i in range(g):
        idx0 = i*n
        idxf = idx0 + n
        if idxf > l:
            idxf = l
        #print(idx0, idxf)
        pars.append([idx0, idxf])
    return pars


## GRAFICOS CON n barras
## Usaremos un parámetro n para distribuir los dias de mes
## en grupos de n días.
n = 7

anho = d.fecha.dt.year.to_list()[0]
meses = d.fecha.dt.month
d["mes"] = meses
dias_ = d.fecha.dt.day
d["diames"] = dias_

#d = d[d.mes < 3] #prueba
if plot_daily:
    for i in d.mes.unique():
        title = f"{calendar.month_name[i]} - {anho}"
        fname = f"{calendar.month_abbr[i]}_{anho}.png"
        a = d[d.mes == i]
        grps = int(len(a)/n) #grupos
        extr = len(a)%n      #sobrantes, si extr>0 se hace un piso más
        #print(len(a), grps, extr)
        if extr > 0:
            grps = grps + 1
        idxs = gen_idx(len(a), n, grps)
        a_dias = a.diames.to_list()
        a_manual = a.manual.to_list()
        a_auto = a.automatico.to_list()
        fig, ax = plt.subplots(grps, 1, figsize = (6, 8))
        for k in range(grps):
            idxf = idxs[k][1]
            idx0 = idxs[k][0]
            pha = np.zeros(len(a_dias[idx0:idxf])) + .125
            ax[k].bar(a_dias[idx0:idxf] - pha, a_manual[idx0:idxf], color = "g", width = 0.25, label = "Manual")
            ax[k].bar(a_dias[idx0:idxf] + pha, a_auto[idx0:idxf], color = "darkviolet", width = 0.25, label = "Automatico")
        ax[0].legend()
        ax[0].set_title(title)
        fig.supylabel("mm Acumulado diario")
        ax[-1].set_xlabel("Dia del mes")
        fig.savefig(f"figs/daily_plots/{fname}", dpi = 300)
#plt.show()
    

### GRAFICO DE ACUMULADO DIARIO
fig, ax = plt.subplots(1,1, figsize = (6,3))
ax_date = mdates.date2num(d.fecha)
ax.plot(ax_date, np.cumsum(d.manual), label = "Medida manual")
ax.plot(ax_date, np.cumsum(d.automatico), label = "Medida automática")
ax.set_ylabel("Precipitado acumulado [mm]")
ax.set_title("Comparación acumulados diarios")
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
fig.savefig("figs/comparacion_acumulado.png", dpi = 300)