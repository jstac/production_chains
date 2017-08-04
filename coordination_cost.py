
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
from rp import RPline

deltas = np.linspace(1.000001, 1.2, 25)
thetas = np.linspace(0.05, 2, 25)
ds, ts = np.meshgrid(deltas, thetas)

def f(delta, theta):
    cf = lambda x: np.exp(theta * x) - 1
    ps = RPline(n=500, delta=delta, c=cf)
    return ps.p[-1] / theta  # c'(0) = theta

fv = np.vectorize(f)
Z = fv(ds, ts)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.contourf(ds, ts, Z, 8, cmap=cm.jet, alpha=0.4)
C = ax.contour(ds, ts, Z, 8, colors='black', alpha=0.6, linewidth=1.4)
ax.clabel(C, inline=1, fontsize=14)
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(ds, ts, Z, rstride=1, cstride=1, cmap=cm.gray, alpha=0.6, linewidth=0.25)
#ax.set_zlim(150, 200)
ax.set_xlabel(r'$\delta$', fontsize=16)
ax.set_ylabel(r'$\theta$', fontsize=16)
fig.show()
