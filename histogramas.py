import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scienceplots
plt.style.use(["science", "nature"])
## TIPOS DE EVENTO (columna "tipo")
## Tipo 0: Evento marcado manualmente (encontrado en pluvio manual)
## Tipo 1: Evento perdido (encontrado en pluvio automatico pero no manual)
## Tipo 2: No precipitado (ni en manual ni en automatico)

plot_boxes = True
threshold = True
d = pd.read_csv("outputs/all_events.csv")
d = d[(d.tipo == 0) | (d.tipo == 1)]

#creando barras centradas en cada duración
bins = np.arange(1, d.duracion.max() + 1.5) - 0.5

dd = d[d.duracion == 11]
print(dd)


#getting max and min measurements
mx = max([d.precip.max(), d.pluvio.max()]) + 0.5
mn = min([d.precip.min(), d.pluvio.min()]) - 0.5

fig, ax = plt.subplots(3,1, figsize = (6,10), sharex=True)
plt.subplots_adjust(hspace=0.02)
ax[0].hist(d.duracion, bins = bins)
ax[0].set_ylabel("Cantidad")
ax[1].scatter(d.duracion, d.pluvio)
ax[1].set_ylabel("mm (manual)")
ax[1].set_ylim(mn, mx)
ax[2].scatter(d.duracion, d.precip)
ax[2].set_ylabel("mm (automatico)")
ax[2].set_ylim(mn, mx)
ax[2].set_xticks(bins + 0.5)
ax[2].set_xlabel("Duración de eventos [horas]")
ax[0].set_title("Eventos marcados (0) y perdidos (1)")
fig.savefig("figs/comparison_events.png", dpi = 300)
plt.show()


# AHORA EL ANALISIS DE TODOS LOS EVENTOS
df = d.copy()
diferencia = df.pluvio - df.precip
df["diferencia"] = diferencia
observers = df.observador.unique()

import matplotlib.pyplot as plt
# Cantidad de eventos registrados por observador
bxdata = []; names_wcount = []; obs_names = []; dfs = []
for j in observers:
    aux = df[df.observador == j]
    print(j, len(aux))
    if len(aux) >= threshold:
        bxdata.append(aux.diferencia)
        names_wcount.append(f"{j}-{len(aux)}")
        obs_names.append(j)

if plot_boxes:

    fig, ax = plt.subplots(1,1, figsize = (10,6))
    ax.boxplot(bxdata)
    ax.axhline(0, c = "k", lw = 0.5, alpha = .5)
    #ax.set_xticklabels(obs_names) #nombres y conteo
    ax.set_xticklabels(names_wcount) #solo nombres
    ax.set_title("Diferencia de medidas por observador")
    ax.set_ylabel("mm de diferencia (manual - auto)")
    fig.savefig("figs/boxplot_new.png")


    plt.show()
