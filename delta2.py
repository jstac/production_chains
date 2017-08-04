
"""
Investigates relationship between delta and p(1) (i.e., price at 1)

"""

from __init__ import *
import line

deltas = np.linspace(0.995, 0.999, num=10)
prices = []

ps = line.PS(c = lambda x: x**4)

for delta in deltas:
    ps.set_delta(delta)
    prices.append(ps.q[ps.n-1])

plt.plot(deltas, prices)

plt.show()

