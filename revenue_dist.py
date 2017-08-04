
"""
Computes distribution of firm size, as measured by revenue

John Stachurski, May 2012.

"""

from __init__ import *
from line import PS

#cost_fun = lambda t:  t + (20 * t)**1.4 
tau = 0.001
quantile = 0.5
cost_fun = lambda t:  np.exp(t**2) - 1
S = 10
num_bins = 10

ps = PS(n=500, tau=tau, c=cost_fun, S=S)

stages = ps.compute_stages()
#print "number of firms =", len(stages)
# Drop the last one, which is zero
stages.pop()
# Compute revenue
rv = [ps.q_func(s) for s in stages]
# Some have measured revenue of zero, so set them to the minimum of the
# positive values in rv
minpos = min(r for r in rv if r > 0)
rv = np.array([max(r, minpos) for r in rv])
# Discard observations below the x% quantile (left hand tail of small firms)
rv.sort()
k = int(len(rv) * quantile)
#print "median =", rv[k]
rvt = [r for r in rv if r > rv[k]]
rvt = np.array(rvt)

freq, bins, patches = plt.hist(rvt, bins=num_bins)
plt.clf()
x = np.log(bins[1:])
y = np.log(freq + 1e-10)
slope, intercept = np.polyfit(x, y, 1)
#print "intercept = ", intercept
#print "slope = ", slope
#print "alpha = ", - slope - 1
yp = np.polyval((slope, intercept), x)
plt.plot(x, y, '.')
plt.plot(x, yp, '-')
plt.show()
