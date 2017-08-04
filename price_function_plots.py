"""
John Stachurski, 2012.

Plots prices and / or firm boundaries

"""

from __init__ import *
from rp import RPline
from matplotlib import rc

rc('text', usetex=True)
rc('font', family="serif", serif="palatino")


delta = 1.02
theta = 10
cost_fun = lambda x:  np.exp(theta * x) - 1
ps = RPline(n=1000, delta=delta, c=cost_fun)

if 0:  # Plot just prices
    delta = 1.02
    ps.set_delta(delta)
    plt.plot(ps.grid, ps.p, 'k--', label="$p^*$ when $\delta = 1.02$")
    #z = 1 + 8 * theta / np.log(1 + tau)
    #print "analytical N* = ", 0.5 * (1 + np.sqrt(1 + z))

    delta = 1.2
    ps.set_delta(delta)
    plt.plot(ps.grid, ps.p, 'k-', label="$p^*$ when $\delta = 1.2$")
    #z = 1 + 8 * theta / np.log(1 + tau)
    #print "analytical N* = ", 0.5 * (1 + np.sqrt(1 + z))

    plt.xlabel("production stage", fontsize=14)
    plt.ylabel("price", fontsize=14)
    plt.yticks((5, 15, 25, 35))
    plt.xticks((0.0, 0.25, 0.75, 1.0))


if 0:  # Plot prices and actions -- one panel

    fig, ax = plt.subplots()
    delta = 1.05
    ps.set_delta(delta)
    ax.plot(ps.grid, ps.p, 'k-', lw=2, alpha=0.65)
    ts = ps.compute_stages()
    for s in ts:
        ax.axvline(x=s, c="0.5")

    plt.yticks((4, 8, 12, 16))
    plt.xticks((0.0, 1.0))
    plt.ylabel("price")
    plt.xlabel("production stage")

if 1:  # Plot prices and actions -- two panels

    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    delta = 1.02
    ps.set_delta(delta)
    ax.plot(ps.grid, ps.p, 'k-', lw=2, alpha=0.65)
    ts = ps.compute_stages()
    for s in ts:
        ax.axvline(x=s, c="0.5")
    plt.yticks((4, 8, 12, 16))
    plt.xticks((0.0, 1.0))
    plt.ylabel("price")

    ax = fig.add_subplot(2,1,2)
    delta = 1.20
    ps.set_delta(delta)
    ax.plot(ps.grid, ps.p, 'k-', lw=2, alpha=0.65)
    ts = ps.compute_stages()
    for s in ts:
        ax.axvline(x=s, c="0.5")
    plt.yticks((5, 15, 25, 35))
    plt.xticks((0.0, 1.0))
    plt.xlabel("production stage")
    plt.ylabel("price")

plt.legend(loc=0)

plt.show()
