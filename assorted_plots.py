"""
Plots used for the JET revision.

August 2014

"""
from rp import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# == Empirical data from Compustat == #
year = 2013
filename = 'compustat_data/USsales_{0}.csv'.format(year)
df = pd.read_csv(filename) 
sales = df['sales'] * (10**6) # unit = US Dollars
empirical_obs = sorted(sales, reverse=True)

# == Model parameters == #
def c(x):
    return np.exp(10 * x**2) - 1
ps = RPline(c=c, delta=1.01)

# == Calculate different measures of firm size == #
stages = ps.compute_stages()
rev = ps.p_func(stages)

# == Compute step size and value added of each firm == #
J = len(stages)
va = np.empty(J-1)
steps = np.empty(J-1)
for i in range(J):
    if i + 1 < J:
        va[i] = ps.p_func(stages[i]) - ps.p_func(stages[i+1])
        steps[i] = stages[i] - stages[i+1]
empl = c(steps)

# == Select which size measure to use == #
obs = rev * (empirical_obs[0] / rev[0]) 
# obs = va
#obs = np.asarray(empirical_obs)

# == Print summary statistics == #
#print "no of firms: ", len(obs)
#print "mean: ", obs.mean()
#print "median: ", np.median(obs)
#print "sd: ", obs.std()
q = obs.mean() + 2 * obs.std()
#print "fraction of sample > m + 2s: ", np.mean(obs > q)
#print "mean / median: ", np.mean(obs) / np.median(obs)


# == Setup for figures == #

# == Zipf plot == #
if 1: 
    fig, ax = plt.subplots(figsize=(10, 6.0))
    z = np.log(obs[:-1])
    mu, sd = z.mean(), z.std()
    Z = mu + sd * np.random.randn(len(obs))
    ln_obs = np.exp(Z)
    ln_obs = np.sort(ln_obs)[::-1]
    ax.set_xlabel('log rank', fontsize=14)
    ax.set_ylabel('size', fontsize=14)
    ax.loglog(np.arange(len(obs)) + 1, obs, 'bo', label="observations")
    ax.loglog(np.arange(len(ln_obs)) + 1, ln_obs, 'rp', alpha=0.3,
        label="lognormal approximation")
    ax.legend(frameon=False)

# == Histogram == #
if 0:
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    ax = axes[0]
    ax.hist(va, bins=26, label="value added")
    ax.set_xlim(0, 1.1 * max(va))
    ax = axes[1]
    ax.hist(empl, bins=26, label="employment")
    ax.set_xlim(0, 1.1 * max(empl))
    ax = axes[2]
    ax.hist(rev, bins=26, label="revenue")
    ax.set_xlim(0, 1.1 * max(rev))
    for ax in axes:
        ax.legend(frameon=False, fontsize=14)
        ax.set_ylabel("number of firms", fontsize=14)
        ax.set_yticks((0, 50, 100, 150))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))


plt.show()
