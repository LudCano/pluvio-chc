import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
    
fname = "outputs/all_events.csv"
plot_boxes = True
date_start = "2023-01-01"
date_fin = "2024-02-01"
filter_type = True
# AHORA EL ANALISIS DE TODOS LOS EVENTOS
df = pd.read_csv(fname)
diferencia = df.pluvio - df.precip
diferenciaconi = df.conico - df.precip
df["diferencia"] = diferencia
df["diferenciaconi"] = diferenciaconi
observers = df.observador.unique()

if filter_type:
    df = df[(df.tipo == 0) | (df.tipo == 1)]

import matplotlib.pyplot as plt
def plt_obs(obs, bxdata, bxdata2):
    pth = f'figs/by_observer/{obs}'
    fig, ax = plt.subplots()
    plt.subplots_adjust(hspace=.2)
    ax.boxplot([bxdata, bxdata2])
    ax.axhline(0, c = "k", lw = 0.5, alpha = .5)
    #ax.set_xticklabels(obs_names) #nombres y conteo
    ax.set_xticklabels(['Conico', 'Cilindrico']) #solo nombres
    ax.set_ylabel("Diferencia con automatico")
    ax.set_title(f"Diferencia entre medidas\n{j}")
    fig.savefig(f"{pth}/boxplot_comparison_2.png")
    tst_file = open(f'{pth}/tests.txt', 'a')
    model = st.wilcoxon(bxdata, bxdata2)
    print(model, file = tst_file)
    x = sm.add_constant(bxdata2)
    model = sm.OLS(bxdata, x).fit()
    print(model.summary(), file = tst_file)

def other_tests(obs, conic, cilind):
    pth = f'figs/by_observer/{obs}'
    tst_file = open(f'{pth}/tests_pluv.txt', 'a')
    model = st.wilcoxon(conic, cilind)
    print(model, file = tst_file)
    x = sm.add_constant(cilind)
    model = sm.OLS(conic, x).fit()
    print(model.summary(), file = tst_file)

# Cantidad de eventos registrados por observador
bxdata = []; names_wcount = []; obs_names = []; dfs = []
bxdata2 = []
for j in observers:
    aux = df[df.observador == j]
    print(j, len(aux))
    if len(aux) >= 1:
        bxdata.append(aux.diferencia)
        bxdata2.append(aux.diferenciaconi)
        names_wcount.append(f"{j}")
        obs_names.append(j)
        plt_obs(j, aux.diferencia, aux.diferenciaconi)
        other_tests(j, aux.pluvio, aux.conico)
if plot_boxes:
    fig, ax = plt.subplots(2, 1, sharey= True, figsize = (9,4))
    plt.subplots_adjust(hspace=.2)
    ax[0].boxplot(bxdata)
    ax[1].boxplot(bxdata2)
    ax[0].axhline(0, c = "k", lw = 0.5, alpha = .5)
    ax[1].axhline(0, c = "k", lw = 0.5, alpha = .5)
    #ax.set_xticklabels(obs_names) #nombres y conteo
    ax[-1].set_xticklabels(names_wcount) #solo nombres
    ax[0].set_ylabel("Diferencia CILIND")
    ax[1].set_ylabel("Diferencia CONIC")
    ax[0].set_title(f"Diferencia entre medidas\n{date_start} al {date_fin}")
    ax[0].set_xticks([])
    fig.savefig("figs/boxplot_test.png")


    #plt.show()