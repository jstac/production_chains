"""
John Stachurski, 2012.

"""

from __init__ import *
from rp import RPline

tau = 0.05
delta = 1 + tau
theta = 2
cost_fun = lambda x:  np.exp(theta * x) - 1
#cost_fun = lambda x:  x + x**1.01

ps = RPline(n=1000, tau=tau, c=cost_fun)

stages = ps.compute_stages()
steps = -np.diff(stages, 1)

print "N* from compute_stages =", len(steps)

z = 1 + 8 * theta / np.log(delta)
print "analytical N* = ", 0.5 * (1 + np.sqrt(1 + z))



