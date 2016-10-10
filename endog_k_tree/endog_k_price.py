r"""
Computes equilibrium prices and actions for the
functional equation

    p(s) = min_{k \in \NN, t <= s} { delta k p(t/k) + c(s - t) + beta k }

"""

import numpy as np
from scipy.optimize import fminbound
import matplotlib.pyplot as plt


class RP:
    
    def __init__(self, 
            n=500, 
            delta=1.01, 
            beta=0.1, 
            c=lambda x: np.exp(3 * x) - 1):

        self.n = n
        self.delta = delta
        self.beta = beta
        self.c = c

    def set_prices(self):
        self.grid = np.linspace(0, 1, num=self.n)
        self.p = self.compute_prices()  
        self.p_func = lambda x: np.interp(x, self.grid, self.p)  

    def solve_min(self, p, s, kmax=10):
        """
        Solve for minimum and minimizers when at stage s, given p.

        The parameter p should be supplied as a function.

        """
        current_function_min = np.inf
        delta, beta, c, n = self.delta, self.beta, self.c, self.n

        for k in range(1, kmax+1):
            def Tp(ell): 
                return delta * k * p((s - ell)/ k) + c(ell) + beta * (k - 1)

            ell_star_eval_at_k = fminbound(Tp, 0, s)
            function_value = Tp(ell_star_eval_at_k)

            if function_value < current_function_min:
                current_function_min = function_value
                k_star = k
                ell_star = ell_star_eval_at_k

        return current_function_min, k_star, ell_star

    def apply_T(self, current_p):
        delta, beta, c, n = self.delta, self.beta, self.c, self.n
        p = lambda x: np.interp(x, self.grid, current_p)
        new_p = np.empty(n)

        for i, s in enumerate(self.grid):
            current_function_min, k_star, ell_star = self.solve_min(p, s)
            new_p[i] = current_function_min

        return new_p


    def compute_prices(self, tol=1e-4, verbose=False):
        """
        Iterate with T.  The initial condition is p = c.
        """
        delta, beta, c, n = self.delta, self.beta, self.c, self.n
        current_p = c(self.grid)  # Initial condition is c
        error = tol + 1
        while error > tol:
            new_p = self.apply_T(current_p)
            error = np.max(np.abs(current_p - new_p))
            if verbose == True:
                print(error)
            current_p = new_p
        return new_p


    def plot_prices(self, plottype='-', label=None):
        plt.plot(self.grid, self.p, plottype, label=label)




# == Example of usage == #


if __name__ == '__main__':

    ps = RP()
    # levels = ps.compute_stages()
    # ts, ls, vs = [], [], []
    # for level in levels:
        # t, l, v = level
        # ts.append(t)
        # ls.append(l)
        # vs.append(v)
    # # Count the number of firms
    # num_firms = 0
    # for n in range(len(levels)):
        # num_firms += ps.k**n
    # print "Number of firms:", num_firms
    ps.plot_prices()
    plt.show()
""
