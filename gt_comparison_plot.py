import numpy as np
from scipy import stats
from scipy.integrate import quad
import matplotlib.pyplot as plt

def gt_comparison_plot(data, mu=None, sig=None, k=3.3e11, x_c = None):
    """
    Generate the comparison Zipf plot for the data.  

    Parameters
    ----------
    data : array_like
        Size of each firm, where size is measured by sales, value added,
        number of employees or some other variable.
    k : float
        Smoothness parameter in gradually truncated lognormal. Default value
        is from equation (5) of Hari, et al (2007, Physica A)
    x_c : float
        Truncation parameter

    """
    N = len(data)
    log_data = np.log(data)
    sorted_data = sorted(data, reverse=True)  # Largest to smallest
    if mu is None:
        mu = np.mean(log_data)
    if sig is None:
        sig = np.std(log_data)
    norm_rv = stats.norm()

    # === Zipf plot for the log-normal distribution === #
    xvals = lambda i: np.exp(sig * norm_rv.ppf(1 - (i / N)) + mu)

    # rank the companies by data
    rf = [(i+1, x) for i, x in enumerate(sorted_data)]
    # separate the ranking and the data 
    x1, x2 = zip(*(rf))

    if x_c is None:
        # === determine the truncation point: x_c === #
        Tol = 1e5
        for i, x in enumerate(sorted_data):
            if abs(x - xvals(float(i+1))) < Tol:
                break
        x_c = x

    # The probability density function for y <= x_c 
    pdf_1 = lambda y: np.exp(- ((y - mu)**2) / (2 * (sig**2)))
    # The probability density function for y > x_c
    pdf_2 = lambda y: np.exp(- ((y - mu)**2) / (2 * (sig**2))) \
                        * np.exp(- ((np.exp(y) - x_c) / k)**2)

    # === compute the value of the constant C in the density === #

    # compute the integration for [-inf, log(x_c)] 
    lower_1 = mu - 6.0 * sig
    upper_1 = np.log(x_c)
    integral_1, error_1 = quad(pdf_1, lower_1, upper_1)
    # compute the integration for [log(x_c), inf] 
    lower_2 = np.log(x_c)
    upper_2 = mu + 6.0 * sig
    integral_2, error_2 = quad(pdf_2, lower_2, upper_2)
    # Finally,
    C = np.sqrt(2 * np.pi) * sig / (integral_1 + integral_2)

    def gt_lognormal(y):
        """
        The Zipf plot for the Gradually Truncated Log-normal distribution.
        See equation (8) of Hari, etc.(2007, Physica A)

        """
        integrand_1 = lambda y: np.exp(- ((y - mu)**2) / (2 * (sig**2)))
        integrand_2 = lambda y: np.exp(- ((y - mu)**2) / (2 * (sig**2))) \
                                * np.exp(- ((np.exp(y) - x_c) / k)**2)

        constant = N * C / (np.sqrt(2 * np.pi) * sig)

        if y <= np.log(x_c):
            part_1, error_1 = quad(integrand_1, y, upper_1)
            part_2, error_2 = quad(integrand_2, lower_2, upper_2)
            g_y = constant * (part_1 + part_2)
        else:
            part_3, error_3 = quad(integrand_2, y, upper_2)
            g_y = constant * part_3

        return g_y


    # === equation (8) of Hari, etc(2007, Physica A) === #
    rank_of_firms = np.empty(N)
    for i in range(N):
         rank_of_firms[i] = gt_lognormal(np.log(sorted_data[i]))

    # == Plots == #
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlabel('rank', fontsize=14)
    ax.set_ylabel('revenue', fontsize=14)

    # === use log(10) scale on both axes === #
    plt.xscale('log')
    plt.yscale('log')

    # === set the range of the horizontal axis === #
    xmin, xmax = 1.0, N * 1.2
    ax.set_xlim(xmin, xmax)

    # === set the range of the vertical axis === #
    #ymin, ymax = 10.0**2, 10.0**14
    #ax.set_ylim(ymin, ymax)

    # Zipf plot for the log-normal distribution
    grid = np.linspace(xmin, xmax, 400)
    ax.plot(grid, [xvals(r) for r in grid], 'k-', lw=2, alpha=0.8, label='lognormal')

    # Zipf plot for the empirical data
    ax.plot(x1, x2, 'ko', label='empirical', alpha=0.4)

    # Zipf plot for the gradually truncated log-normal distribution
    ax.plot(rank_of_firms, sorted_data, 'b--', lw=2, alpha=0.8, label='G.T. lognormal')
    
    ax.legend(frameon=False, loc='center')
    plt.show()
