
"""
Investigates relationship between tau and price function

"""

from __init__ import *
import line

from matplotlib import rc
rc('text', usetex = True)
rc('font', family='serif')


taus = (0.01, 0.05, 0.1)

ps = line.PS(c = lambda x: np.exp(x**2) - 1)

for tau in taus:
    ps.set_tau(tau)
    ps.plot_prices(plottype='k-')

plt.text(0.77, 0.092, r'$\tau=0.10$', {'color' : 'k', 'fontsize' : 18})
plt.text(0.77, 0.045, r'$\tau=0.05$', {'color' : 'k', 'fontsize' : 18})
plt.text(0.77, 0.01, r'$\tau=0.01$', {'color' : 'k', 'fontsize' : 18})

plt.show()
