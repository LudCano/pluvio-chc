import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(["science", "nature"])
# GETTING STATISTICS
eventos = pd.read_csv("outputs/all_events.csv")
print(eventos.describe())

print(len(eventos[eventos.tipo == 1]))
eventos = eventos[eventos.tipo != 1]

diferencias = []
for i, j in zip(eventos.precip, eventos.pluvio):
    if i != 0:
        dd = 100*(j-i)/i
        if abs(dd) > 10000:
            dd = np.nan
    else:
        dd = np.nan
    diferencias.append(dd)

st = pd.Series(diferencias)
print(st.describe())

diferencias = st[st < 150]

plt.figure()
plt.hist(diferencias, bins = 10)
plt.xlim(-150,150)
plt.xlabel("Diferencia porcentual (auto = 100\%)")
plt.ylabel("Frecuencia")
plt.title("Eventos registrados")
plt.savefig("figs/histo_dif.png", dpi = 300)
#plt.show()


eventos = pd.read_csv("outputs/daily_acum.csv")
a = np.array(np.cumsum(eventos.manual))
print(a[-1])
a = np.array(np.cumsum(eventos.automatico))
print(a[-1])

st = st[st < 200]
print(st.describe())

df2 = pd.read_csv("outputs/all_events.csv")
#df2 = df2[df2.tipo == 1]
df2["horas"] = pd.to_datetime(df2.fechahora)
df2["horas"] = [i.hour for i in df2.horas]

pers = []
lost = []
marked = []
mn = []
for j in range(24):
    aux = df2[df2.horas == j]
    a = aux[aux.tipo == 1]
    b = aux[aux.tipo == 0]
    per = 100*(len(a))/(len(a) + len(b))
    pers.append(per)
    lost.append(len(a))
    marked.append(len(b))
    mn.append(np.mean(a.precip))


fig, ax = plt.subplots(3,1,sharex=True)
ax[0].bar(np.arange(24), lost)
ax[0].set_ylim(0,25)
ax[1].set_ylim(0,25)
ax[1].bar(np.arange(24), marked)
ax[0].set_ylabel("Perdidos")
ax[1].set_ylabel("Marcados")
ax[2].bar(np.arange(24), pers)
ax[2].set_ylabel("\% perdidos")
#plt.xlim(-150,150)
ax[-1].set_xlabel("Hora Local")
#plt.ylabel("Frecuencia")
ax[0].set_title("Hora de eventos")
plt.savefig("figs/histo_hora.png", dpi = 300)



fig, ax = plt.subplots(3,1,sharex=True)

ax[0].bar(np.arange(24), lost)
ax[0].set_ylim(0,25)
ax[1].bar(np.arange(24), mn)
ax[0].set_ylabel("Perdidos")
ax[1].set_ylabel("Precip perdida")
ax[2].bar(np.arange(24), pers)
ax[2].set_ylabel("\% perdidos")

#plt.xlim(-150,150)
ax[-1].set_xlabel("Hora Local")
#plt.ylabel("Frecuencia")
ax[0].set_title("Hora de eventos")
plt.savefig("figs/histo_hora2.png", dpi = 300)
plt.show()