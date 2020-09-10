import math
import numpy as np
import pandas as pd
import scipy.optimize as spo
from enum import Enum


def daily_free_risk():
    return (1.08 ** (1 / 365) - 1.0)


class Statistic(object):
    def __init__(self, column):
        self.cumulative = column.df.ix[-1] - column.df.ix[0]
        self.average = column.df.mean()
        self.risk = column.df.std()
        self.sharpe_ratio = (self.average - daily_free_risk()
                             ) / self.risk * math.sqrt(252)

    def __str__(self):
        text = []
        text.append("Cumulative:")
        text.append(str(self.cumulative))
        text.append("Average:")
        text.append(str(self.average))
        text.append("Risk:")
        text.append(str(self.risk))
        text.append("Sharpe ratio (year):")
        text.append(str(self.sharpe_ratio))
        return "\n".join(text)


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
        self.df = pd.DataFrame()

    def portfolio_val(self, allocates, cost=1.0):
        port = self.normalize() * allocates
        port = port * cost

        dr = port.sum(axis=1)
        dr.name = "Portfolio"
        return dr.to_frame()

    def fit_line(self, error_func):
        column_num = self.df.shape[1]
        init_allocates = np.ones(column_num) / column_num
        limits = ()
        for x in range(column_num):
            limits += ((0.0, 1.0),)

        constr = {'type': 'eq', 'fun': _sum_one}

        result = spo.minimize(error_func, init_allocates, args=(self,),
                              method='SLSQP', bounds=limits,
                              constraints=constr, options={'disp': True})
        return result.x
