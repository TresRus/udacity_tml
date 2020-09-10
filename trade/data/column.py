import numpy as np
import pandas as pd
import scipy.optimize as spo
from enum import Enum


def _sum_one(allocates):
    return np.sum(allocates) - 1.0


class Column(object):
    class Name(Enum):
        DATE = "Date"
        ADJCLOSE = "Adj Close"
        CLOSE = "Close"
        HIGH = "High"
        LOW = "Low"
        OPEN = "Open"
        VOLUME = "Volume"

    def __init__(self, name):
        self.name = name
        self.data = pd.DataFrame()

    def __str__(self):
        return str(self.data)

    def portfolio_val(self, allocates, cost=1.0):
        port = self.normalize() * allocates
        port = port * cost

        dr = port.sum(axis=1)
        dr.name = "Portfolio"
        return dr.to_frame()

    def fit_line(self, error_func):
        column_num = self.data.shape[1]
        init_allocates = np.ones(column_num) / column_num
        limits = ()
        for x in range(column_num):
            limits += ((0.0, 1.0),)

        constr = {'type': 'eq', 'fun': _sum_one}

        result = spo.minimize(error_func, init_allocates, args=(self,),
                              method='SLSQP', bounds=limits,
                              constraints=constr, options={'disp': True})
        return result.x
