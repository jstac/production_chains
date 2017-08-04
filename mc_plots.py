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
c_prime = lambda x: theta * np.exp(theta * x)
ps = RPline(n=1000, c=cost_fun, delta=1.05)
s = 0.25

p_prime = lambda s: c_prime(ps.ell_star(s))

ell_points = np.linspace(0, s, 150)

fig, ax = plt.subplots()
#ax.set_xticks((0.0, 0.25, 0.75, 1.0))
ax.set_ylim(0.0, 40)
ax.set_xlabel(r'$\ell$', fontsize=16)
ax.set_ylabel("marginal cost", fontsize=16)

y1 = [c_prime(ell) for ell in ell_points]
y2 = [ps.delta * p_prime(s - ell) for ell in ell_points]
lb1 = "$c'(\ell)$"
lb2 = "$\delta_0 p_0'(s - \ell)$"
ax.plot(ell_points, y1, 'b-', lw=2, alpha=0.65, label=lb1)
ax.plot(ell_points, y2, 'g-', lw=2, alpha=0.65, label=lb2)

delta = 1.1
lb3 = "$\delta_1 p_0'(s - \ell)$"
y3 = [delta * p_prime(s - ell) for ell in ell_points]
ax.plot(ell_points, y3, 'k--', lw=2, alpha=0.65, label=lb3)
#
ps.delta = delta
lb4 = "$\delta_1 p_1'(s - \ell)$"
y4 = [ps.delta * p_prime(s - ell) for ell in ell_points]
ax.plot(ell_points, y4, 'k-', lw=2, alpha=0.65, label=lb4)

ax.legend(loc=0)
plt.show()
