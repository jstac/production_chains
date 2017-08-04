
from __init__ import *

class Ecdf:

    def __init__(self, data):
        self.data = np.array(data)

    def __call__(self, xvec):
        if isinstance(xvec, float): return(np.mean(self.data <= xvec))
        yvec = []
        for x in xvec: yvec.append(np.mean(self.data <= x))
        return np.array(yvec)


