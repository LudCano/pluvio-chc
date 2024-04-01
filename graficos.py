import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(["science", "nature"])

d = pd.read_csv("outputs/daily_acum.csv")

dd = []
for u, v in zip(d.manual, d.automatico):
    if u == 0 and v == 0:
        dd.append(0)
    elif v == 0 and u != 0:
        dd.append(np.nan)
    else:
        dd_ = 100*(u-v)/v
        dd.append(dd_)

d["d"] = dd
d["d2"] = d.manual - d.automatico
#d = d[d.flg == 1]
#d["d"] = 100*(d.manual - d.automatico)/d.automatico
#d.loc[d.d > 100, "d"] = 100
#print(d.d)

cajas = []
cajas2 = []
o = []
l_o = d.observador.dropna().unique()
perdidos = []
c = 1
xx_a = []
for i in l_o:
    if i == "nan":
        pass
    else:
        a = d[d.observador == i]
        aux = a.d.isna().sum()
        print(i, len(a), aux)
        b = a[a.d.isna()]
        if len(b)>0:
            perdidos.append(b.manual.to_list())
            print(b)
            xx = [c for i in range(len(b))]
            xx_a.append(xx)
        a = a.dropna()
        cajas.append(a.d.to_list())
        cajas2.append(a.d2.to_list())
        o.append(str(i) + " "+ str(aux))
        c = c +1


xx_b = sum(xx_a, [])
todos_perdidos = sum(perdidos, [])


fig2, ax2 = plt.subplots(2,1, sharex=True, height_ratios = [2,1], figsize = (6,5),dpi = 300)
plt.subplots_adjust(hspace=0)
ax2[1].boxplot(cajas)
ax2[0].boxplot(cajas2)
ax2[0].axhline(y = 0, c = "b", alpha = .5, lw = .8)
ax2[0].scatter(xx_b, todos_perdidos, c = "red", marker = "x", s = 15)

ax2[0].set_ylabel("mm de diferencia (manual - auto)")
ax2[1].set_ylabel("diferencia porcentual")
ax2[0].set_title("Comparación medidas 2023 (acumulado diario)")
ax2[1].axhline(y = 0, c = "b", alpha = .5, lw = .8)
ax2[1].set_ylim(-200,200)
ax2[1].set_xticks(range(1,len(o)+1),o)
plt.tight_layout()
fig2.savefig("figs/por_dia.png")


d = pd.read_csv("outputs/all_events.csv")

dd = []
for u, v in zip(d.pluvio, d.precip):
    if u == 0 and v == 0:
        dd.append(0)
    elif v == 0 and u != 0:
        dd.append(np.nan)
    else:
        dd_ = 100*(u-v)/v
        dd.append(dd_)

d["d"] = dd
d["d2"] = d.pluvio - d.precip
#d = d[d.flg == 1]
#d["d"] = 100*(d.manual - d.automatico)/d.automatico
#d.loc[d.d > 100, "d"] = 100
#print(d.d)

cajas = []
cajas2 = []
o = []
l_o = d.observador.dropna().unique()
perdidos = []
c = 1
xx_a = []
for i in l_o:
    if i == "nan":
        pass
    else:
        a = d[d.observador == i]
        aux = a.d.isna().sum()
        print(i, len(a), aux)
        b = a[a.d.isna()]
        perdidos.append(b.pluvio.to_list())
        xx = [c for i in range(len(b))]
        xx_a.append(xx)
        a = a.dropna()
        cajas.append(a.d.to_list())
        cajas2.append(a.d2.to_list())
        o.append(str(i) + " "+ str(aux))
        c = c +1


xx_b = sum(xx_a, [])
todos_perdidos = sum(perdidos, [])

fig2, ax2 = plt.subplots(2,1, sharex=True, height_ratios = [2,1], figsize = (6,5),dpi = 300)
plt.subplots_adjust(hspace=0)

ax2[1].boxplot(cajas)
ax2[0].boxplot(cajas2)
ax2[0].scatter(xx_b, todos_perdidos, c = "red", marker = "x", s = 15)
ax2[0].axhline(y = 0, c = "b", alpha = .5, lw = .8)
ax2[0].set_ylabel("mm de diferencia (manual - auto)")
ax2[1].set_ylabel("diferencia porcentual")
ax2[0].set_title("Comparación medidas 2023 (acumulado por evento)")
ax2[1].axhline(y = 0, c = "b", alpha = .5, lw = .8)
#ax2[1].set_ylim(-200,200)
ax2[1].set_xticks(range(1,len(o)+1),o)
plt.tight_layout()
fig2.savefig("figs/por_evento.png")
#plt.show()


auxiliar = d[d.d > 200]
print(auxiliar)