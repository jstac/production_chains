
"""
Computes distribution of firm size, as measured by in-house production or
value added

This file is largely depreciated but may contain useful code.

John Stachurski, August 2012.

"""

from __init__ import *
from rp import RPline, RPtree
from scipy.stats import linregress, lognorm, norm

k = 1

if k == 1:
    # Get value added for k = 1 case
    ps = RPline(n=1000, delta=1.01, c=lambda x: np.exp(x**2) - 1)
    stages = ps.compute_stages()
    va = []
    steps = []
    for i in range(len(stages) - 1):
        va.append(ps.p_func(stages[i]) - ps.p_func(stages[i+1]))
        steps.append(stages[i] - stages[i+1])
    print "Number of firms =", len(steps)

if k > 1:
    # Get value added for k > 1 case
    ps = RPtree(delta=1.01, c=lambda x: np.exp(2 * x) - 1, k=k)
    levels = ps.compute_stages()
    ts, ls, vs = [], [], []
    for level in levels:
        t, l, v = level
        ts.append(t)
        ls.append(l)
        vs.append(v)
    # Count the number of levels and firms
    num_levels = len(levels)
    num_firms = 0
    for n in range(num_levels):
        num_firms += ps.k**n
    print "Number of firms:", num_firms
    ## Work out value added for each firm, where firms are
    ## enumerated top to bottom and left to right in the vertical tree
    va = []
    for i in range(num_levels):
        for j in range(ps.k**i):
            va.append(vs[i])

# Get rid of any zero values 
obs = [v for v in va if v > 0]
#obs = steps
#obs = [ps.c(s) for s in steps]
obs = np.array(obs)

# Fit lognormal parameters
mu = np.mean(np.log(obs))
sigma = np.std(np.log(obs))
lobs = np.exp(mu + sigma * norm.rvs(size=1000))

fig, ax = plt.subplots()

## Histogram log-log approach
if 0:
    obs.sort()
    # Cut the left-hand tail
    obs_rt = obs[int(0.90 * len(obs)):]
    freq, bins, patches = ax.hist(obs_rt, bins=15)
    if 0.0 in freq:
        print "Some bins contain zero elements"
        import sys
        sys.exit(0)
    data = np.log(bins[1:])
    xdata = np.log(freq)
    ax.clf()
    ax.loglog(bins[1:], freq, '.')

## ECDF approach
if 0:
    n = len(obs)
    obs.sort()
    obs_min = obs[int(0.01 * n)]
    obs_max = obs[int(0.99 * n)]
    obs = np.array(obs)
    G = lambda x: np.mean(obs >= x)
    F = lambda x: np.mean(lobs >= x)
    xgrid = np.linspace(obs_min, obs_max, 60)
    xdata = np.log(xgrid)
    ydata = [np.log(G(x)) for x in xgrid]
    ydata2 = [np.log(F(x)) for x in xgrid]
    #xdata = xgrid
    #ydata = [G(x) for x in xgrid]
    ax.plot(xdata, ydata,'bo', alpha=0.5)
    ax.plot(xdata, ydata2,'ko', alpha=0.5)
    beta1, beta0, r, tt, stderr = linregress(xdata, ydata)
    line = beta1 * xdata + beta0 # regression line
    print "Slope = ", beta1
    ax.plot(xdata, line, 'k-')

## Plain histogram
if 1:
    obs = 100000 * obs
    ax.hist(obs[:-1], bins=20)
    ax.set_xlabel("value added")
    ax.set_ylabel("number of firms")


## Rank-size plot
if 0:
    #obs.sort(reverse=True)
    n = len(obs)
    xdata = np.log(np.arange(len(obs)) + 1)
    ydata = np.log(np.array(obs))
    ax.plot(xdata, ydata,'o', alpha=0.5)
    ax.xlabel("log rank")
    ax.ylabel("log value added")
    #plt.ylim(-15, -12.5)
    # Regression
    #j = 0.90 * n
    #m = 0.995 * n
    #xdata = xdata[j:m]
    #ydata = ydata[j:m]
    #beta1, beta0, r, tt, stderr = linregress(xdata, ydata)
    #line = beta1 * xdata + beta0 # regression line
    #print "Slope = ", beta1
    #plt.plot(xdata, line, 'k-')


plt.show()
