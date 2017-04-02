"""
For a given parameterization of the model, use recusion to 
build a dictionary that gives the structure of the resulting network.

@author: John Stachurski

@date: Mon Oct 10 12:59:24 JST 2016

"""

from endog_k_price import RP
import numpy as np
import networkx as nx

class Firm:

    def __init__(self, va):

        self.val_add = va
        self.subcontractors = []

    def print(self):
        out = "value added {} and subcontractors ".format(self.val_add)
        print(out)
        print(self.subcontractors)




def build_dict(ps, verbose=False, tol=1e-2):

    s = 1 
    level = 1
    num_firms_at_this_level = 1
    current_firm_num = 1
    first_firm_at_level = 1


    firms = {}
        
    while 1:
        
        # == determine actions and value added of firm at this level == #
        fmin, k_star, ell_star = ps.solve_min(ps.p_func, s) 
        va = ps.c(ell_star) + ps.beta * (k_star - 1)
        
        if verbose == True:
            print("current_firm_num={}".format(current_firm_num))
            print("level={}".format(level))
            print("k={}".format(k_star))    
            print("first_firm_at_current_level={}".format(first_firm_at_level))
            print("num_firms_at_this_level={}".format(num_firms_at_this_level))
            print("")

        # == add firms to dict == #
        for i in range(num_firms_at_this_level):
            firms[first_firm_at_level + i] = Firm(va)

        if s < tol:
            break

        # Otherwise add subcontractors

        for i in range(num_firms_at_this_level):
            for k in range(k_star):
                current_firm_num += 1
                firms[first_firm_at_level + i].subcontractors.append(current_firm_num)

        # == next level values == #
        first_firm_at_level = first_firm_at_level + num_firms_at_this_level
        level += 1
        num_firms_at_this_level *= k_star
        s = (s - ell_star) / k_star

    return firms


def build_dict_and_graph(ps, verbose=False):
    firms = build_dict(ps, verbose=verbose)
    G = nx.Graph()

    for firm_no, firm in firms.items():
        for sub in firm.subcontractors:
            G.add_edge(firm_no, sub)
    return firms, G

