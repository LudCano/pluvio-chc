# COMPARISON OF CONIC AND CYLINDRICAL PLUVIOMETRIES
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
import scienceplots
plt.style.use(['science', 'nature'])


d = pd.read_csv('outputs/processed.csv')
filter_outlier = True
do_plots = False

# Incongruent dates, check manually
#f = open('dates_check.txt', 'w+')
#print(d[d.conico == 0], file = f)
#print("----OUTLIERS---", file = f)
#print(d[(d.d_pluv < -10) | (d.d_conic < -10)], file = f)

if filter_outlier:
    d = d[(d.d_pluv > -10) & (d.d_conic > -10)]

## Statistics
conic = np.array(d.conico)
cilind = np.array(d.pluvio)
auto = np.array(d.acum)

fig, ax = plt.subplots(3,1, sharex = True, sharey = True)
bns = np.arange(0,25,1)
ax[0].hist(conic, bins = bns, label = 'Conico')
ax[1].hist(cilind, bins = bns, label = 'Cilindrico')
ax[2].hist(auto, bins = bns, label = 'Automatico')
ax[0].legend()
ax[1].legend()
ax[2].legend()
fig.supylabel('Conteo')
ax[-1].set_xlabel('Precipitación [mm]')
fig.savefig('figs/histograms_all.png', dpi = 300)
#plt.show()


model = st.wilcoxon(conic, cilind)
print(model)
model = st.wilcoxon(auto, conic)
print(model)
model = st.wilcoxon(auto, cilind)
print(model)



import statsmodels.api as sm
x = sm.add_constant(conic)
model = sm.OLS(cilind, x).fit()
print(model.summary())


def scatter_hist(x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y)

    ax_histx.hist(x, bins=20)
    ax_histy.hist(y, bins=20, orientation='horizontal')

# Start with a square Figure.
fig = plt.figure(dpi = 200)
# Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
# the size of the marginal axes and the main axes in both directions.
# Also adjust the subplot parameters for a square plot.
gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                    left=0.1, right=0.9, bottom=0.1, top=0.9,
                    wspace=0.05, hspace=0.05)
# Create the Axes.
ax = fig.add_subplot(gs[1, 0])
ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
# Draw the scatter plot and marginals.
scatter_hist(conic, cilind, ax, ax_histx, ax_histy)
ax.set_xlabel('Pluvio conico [mm]')
ax.set_ylabel('Pluvio cilindrico [mm]')
fig.savefig('figs/comparacion_pluvios_mm.png', dpi = 350)