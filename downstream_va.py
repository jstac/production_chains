
"""
Plots downstreamness against value added.   x values are the
upstream boundaries of the firms, and y values are the corresponding
firm's value added.

John Stachurski, August 2012.

"""

from __init__ import *
from rp import RPline, RPtree

ps = RPline(n=1000, tau=0.02, c=lambda x: np.exp(10 * x) - 1)
stages = ps.compute_stages()
va = []
rel_va = []
steps = []
for i in range(len(stages) - 1):
    va.append(ps.p_func(stages[i]) - ps.p_func(stages[i+1]))
    rel_va.append(ps.p_func(stages[i]) - ps.p_func(stages[i+1]) / ps.p_func(stages[i]))
    steps.append(stages[i] - stages[i+1])
print "Number of firms =", len(steps)

ydata = [v / ps.p_func(1) for v in va]
#ydata = [ps.c(s) for s in steps]
plt.plot(ydata,'bo')

plt.xlabel("upstreamness")
#plt.ylabel("value added")
plt.ylabel("value added per dollar of output")


plt.show()
