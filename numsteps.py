
"""
Investigates relationship between delta number of trades/steps/firms

"""

from __init__ import *
import line

k = 20  # number of deltas

deltas = np.linspace(0.95, 0.9999, num=k)
nums = []



ps = line.PS(c = lambda x: x**4)

for delta in deltas:
    ps.set_delta(delta)
    ps.compute_stages()
    nums.append(len(ps.transaction_stages))

plt.plot(deltas, nums)

