import pandas as pd

# Ruta final
date_start = "2023-01-01"
date_fin = "2023-12-31"
fname = "outputs/all_events.csv"
plot_boxes = True
threshold = 1

from check_cache import check_cache
proc_again = check_cache(date_start, date_fin)

if proc_again:
    ## PREPROCESO
    from procesamiento import *
    proc_automatic()
    proc_manual()

    ## OBTENIENDO EVENTOS MANUALES
    from merging import merging
    merging(date_start, date_fin)

    ## EVENTOS PERDIDOS
    from perdidos import lost_events
    lost_events(date_start, date_fin, False)

    ## TABLA FINAL
    from complete_proc import complete_table
    complete_table(date_start, date_fin)

    ## ACUMULADOS DIARIOS
    from daily_acum import daily_acum
    daily_acum(date_start, date_fin)
else:
    pass


# AHORA EL ANALISIS DE TODOS LOS EVENTOS
df = pd.read_csv(fname)
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

    fig, ax = plt.subplots(1,1)
    ax.boxplot(bxdata)
    ax.axhline(0, c = "k", lw = 0.5, alpha = .5)
    #ax.set_xticklabels(obs_names) #nombres y conteo
    ax.set_xticklabels(names_wcount) #solo nombres
    ax.set_ylabel("p_obs - p_auto")
    ax.set_title(f"Diferencia entre medidas\n{date_start} al {date_fin}")
    fig.savefig("outputs/boxplot1.png")


    plt.show()