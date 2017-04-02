r"""

Plotting utilities for the network graphs

@author: John Stachurski

@date: Mon Oct 10 12:59:24 JST 2016

"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import linregress

from endog_k_price import RP
from graph_builder import *

from networkx.drawing.nx_agraph import graphviz_layout


def get_value_added(ps, scale_factor=2000):

    firms, G = build_dict_and_graph(ps)
    
    vas = []
    for firm in firms.values():
        vas.append(firm.val_add * scale_factor)

    return vas

def draw_graph(ps, scale_factor=2000, figsizes=(15, 15)):
    
    firms, G = build_dict_and_graph(ps)
    pos = graphviz_layout(G, prog='twopi') # twopi or dot

    fig, ax = plt.subplots(figsize=figsizes)
    ax.axis('off', frame_on=False)

    vas = []
    for firm in firms.values():
        vas.append(firm.val_add * scale_factor)

    nx.draw(G, 
            pos, 
            ax=ax,
            node_size=vas, 
            node_shape='o',
            alpha=0.4, 
            node_color="blue", 
            with_labels=False)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

def show_zipf_plot(ps, scale_factor=2000):
    
    vas = get_value_added(ps, scale_factor=scale_factor)
    rank = np.arange(len(vas)) + 1
    
    fig, ax = plt.subplots(figsize=(10, 6.0))
        
    z = np.log(vas[:-1])
    mu, sd = z.mean(), z.std()
    Z = mu + sd * np.random.randn(len(vas))
    ln_obs = np.exp(Z)
    ln_obs = np.sort(ln_obs)[::-1]
    ax.loglog(np.arange(len(ln_obs)) + 1, ln_obs, 'rp', alpha=0.3,
        label="lognormal approximation")
    

    
    ax.set_xlabel('log rank', fontsize=14)
    ax.set_ylabel('log size', fontsize=14)
    ax.loglog(rank, vas, 'bo', label="observations")

    
    ax.legend(frameon=False)


def zipf_with_regression(ps, scale_factor=2000):
        
    vas = get_value_added(ps, scale_factor=scale_factor)
    rank = np.arange(len(vas)) + 1

    fig, ax = plt.subplots(figsize=(10, 6.0))
    
    n = len(vas)
    xdata = np.log(rank)
    ydata = np.log(np.array(vas))
    ax.plot(xdata, ydata,'o', markersize=15, alpha=0.5)
    ax.set_xlabel("log rank")
    ax.set_ylabel("log value added")
    #plt.ylim(-15, -12.5)
    # Regression
    #j = 0.90 * n
    #m = 0.995 * n
    #xdata = xdata[j:m]
    #ydata = ydata[j:m]
    beta1, beta0, r, tt, stderr = linregress(xdata, ydata)
    line = beta1 * xdata + beta0 # regression line
    lb = "Slope = {}".format(round(beta1, 2))
    ax.plot(xdata, line, 'k-', label=lb)
    ax.legend(loc='upper right')



