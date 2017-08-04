"""
John Stachurski, 2012.

Plots prices and / or firm boundaries

"""

from __init__ import *
from rp import RPline
from matplotlib import rc

theta = 10
cost_fun = lambda x:  np.exp(theta * x) - 1
ps = RPline(n=1000, delta=1.1, c=cost_fun)

fig, ax = plt.subplots()
ax.plot(ps.grid, ps.p, 'k-')
ts = ps.compute_stages()
for s in ts:
    ax.axvline(x=s, c='0.5', lw=2, alpha=0.6)
ax.set_yticks((10, 20, 30))
ax.set_xticks((0.0, 1.0))
ax.set_ylabel("price")
ax.set_xlabel("production stages")
ax.legend(loc=0)

fig.show()

