"""
Computes tree figure, with size of node proportional to value added

John Stachurski, August 2012.

NOTES: Try delta=1.01 and c(x)=np.exp(x) - 1 vs delta=1.1 and c(x)=np.exp(2 * x) -
1.  Same number of firms but different pattern for value added.  Because of
more convexity in the price function?

"""

from __init__ import *
from rp import RPtree
import networkx as nx
import numpy as np

model1 = { 'delta' : 1.02, 'c' : lambda x: np.exp(4 * x) - 1, 'k' : 2 }
model2 = { 'delta' : 1.20, 'c' : lambda x: np.exp(4 * x) - 1, 'k' : 2 }
model3 = { 'delta' : 1.01, 'c' : lambda x: np.exp(2 * x) - 1, 'k' : 2 }
model4 = { 'delta' : 1.05, 'c' : lambda x: np.exp(2 * x) - 1, 'k' : 2 }
model5 = { 'delta' : 1.01, 'c' : lambda x: np.exp(x) - 1, 'k' : 3 }
model6 = { 'delta' : 1.05, 'c' : lambda x: np.exp(x) - 1, 'k' : 3 }
model7 = { 'delta' : 1.01, 'c' : lambda x: np.exp(2 * x) - 1, 'k' : 3 }
model8 = { 'delta' : 1.15, 'c' : lambda x: np.exp(x**1.01) - 1, 'k' : 6 }
model9 = { 'delta' : 1.15, 'c' : lambda x: np.exp(x**1.00) - 1, 'k' : 6 }

# Set the model
model = model1
fig, ax = plt.subplots()

ps = RPtree(delta=model['delta'], c=model['c'], k=model['k'])

levels = ps.compute_stages()
ts, ls, vs = [], [], []
i = 0
for level in levels:
    t, l, v = level
    ts.append(t)
    ls.append(l)
    vs.append(v)
    print "level:", i, "; sum va:", sum(vs)
    i += 1
# Count the number of levels and firms
num_levels = len(levels)
num_firms = 0
for n in range(num_levels):
    num_firms += ps.k**n
print "Number of firms:", num_firms

## Work out value added for each firm, where firms are
## enumerated top to bottom and left to right in the vertical tree
value_added = []
for i in range(num_levels):
    for j in range(ps.k**i):
        value_added.append(vs[i])
# Now rescale value added relative to first one
value_added = [250 * (v / value_added[0]) for v in value_added]
value_added = np.array(value_added)
# Make the smallest value at least 2% of the largest
temp = value_added.max() * 0.02
value_added = np.where(value_added < temp, temp, value_added)


G = nx.balanced_tree(ps.k, num_levels - 1)  
pos = nx.graphviz_layout(G, prog='dot') # twopi or dot
ax.axis('off', frame_on=False)
nx.draw(G, 
        pos, 
        ax=ax,
        node_size=value_added, 
        node_shape='o',
        alpha=0.8, 
        node_color="blue", 
        with_labels=False)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

fig.show()


#plt.savefig('circular_tree.png')
#for i in range(num_firms):
#    x, y = pos[i]
#    x = x * np.random.uniform(low=0.98, high=1.02)
#    y = y * np.random.uniform(low=0.98, high=1.02)
#    pos[i] = (x, y)




