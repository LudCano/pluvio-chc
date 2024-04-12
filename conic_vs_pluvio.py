# COMPARISON OF CONIC AND CYLINDRICAL PLUVIOMETRIES
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import numpy as np
import scienceplots
plt.style.use(['science', 'nature'])


d = pd.read_csv('outputs/processed.csv')
filter_outlier = True
do_plots = False

# Incongruent dates, check manually
f = open('dates_check2.txt', 'w+')
print(d[d.conico == 0], file = f)
print("----OUTLIERS---", file = f)
print(d[(d.d_pluv < -10) | (d.d_conic < -10)], file = f)

if filter_outlier:
    d = d[(d.d_pluv > -10) & (d.d_conic > -10)]

if do_plots:
    fig, ax = plt.subplots()
    ax.hist(d.d_conic, histtype=u'step', bins = 20, label = 'Conico')
    ax.hist(d.d_pluv, histtype=u'step', bins = 20, label = 'Cilindrico')
    ax.set_xlabel('Manual - Automatico (mm)')
    ax.set_ylabel('Cantidad de eventos')
    ax.legend()
    fig.savefig('figs/histogram_conic_cilindrical.png', dpi = 350)
    #plt.show()


    fig, ax = plt.subplots()
    ax.scatter(d.d_conic, d.d_pluv)
    ax.set_xlabel('Manual - Automatico (mm)')
    ax.set_ylabel('Cantidad de eventos')
    ax.legend()
    fig.savefig('figs/scatter_conic_cilindrical.png', dpi = 350)
    #plt.show()


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
    scatter_hist(d.d_conic, d.d_pluv, ax, ax_histx, ax_histy)
    ax.set_xlabel('Diferencia conico [mm]')
    ax.set_ylabel('Diferencia cilindrico [mm]')
    fig.savefig('figs/comparacion_pluvios.png', dpi = 350)
    #plt.show()


## Statistics
import scipy.stats as st
x = np.array(d.d_conic)
xx = np.array(d.d_conic)
y = np.array(d.d_pluv)
model = st.ttest_rel(x, y)
print(model)
model = st.wilcoxon(x, y)
print(model)

print(np.mean(x), np.mean(y), abs(np.mean(x)-np.mean(y)))

import statsmodels.api as sm
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
print(model.summary())


fig, axs = plt.subplots(1,2, figsize = (8,4), dpi = 300)
sm.qqplot(y, line = '45', ax = axs[0], ylabel = 'Cuartiles Cilindrico')
sm.qqplot(xx, line = '45', ax = axs[1], ylabel = 'Cuartiles Conico')
fig.savefig('figs/qqplots.png', dpi = 300)
#plt.show()
