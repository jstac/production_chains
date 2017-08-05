"""
John Stachurski, 2012.

Plots prices and / or firm boundaries

"""

from __init__ import *
from rp import RPline
from matplotlib import rc

rc('text', usetex=True)
rc('font', family="serif", serif="palatino")


theta = 10
cost_fun = lambda x:  np.exp(theta * x) - 1
ps = RPline(n=1500, c=cost_fun)

fig, ax = plt.subplots()
ax.set_xticks((0.0, 0.25, 0.75, 1.0))

ps.delta = 1.02
y_vals = [ps.ell_star(s) for s in ps.grid]
ax.plot(ps.grid, y_vals, 'k--', lw=2, alpha=0.65, label="$\ell^*$ when $\delta = 1.02$")
ax.set_xlabel("production stage", fontsize=12)
ax.set_ylabel("range of tasks", fontsize=12)

ps.delta = 1.2
y_vals = [ps.ell_star(s) for s in ps.grid]
ax.plot(ps.grid, y_vals, 'k-', lw=2, alpha=0.65, label="$\ell^*$ when $\delta = 1.2$")

ax.legend(loc=0)
plt.show()
