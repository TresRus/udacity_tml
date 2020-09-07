import os
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

    def __init__(self, column):
        self.column = column
        self.df = pd.DataFrame()

    def get_date_range(self, dates):
        c = Column(self.column)
        c.df = pd.DataFrame(index=dates)
        c.df = c.df.join(self.df, how="inner")
        return c

    def set_baseline(self, ticker):
        if ticker not in self.df.columns:
            raise ValueError( "No {} ticker in {} column".format(ticker, self.column) )

        # All the missing dates are not interesting for calculations.
        self.df = self.df.dropna(subset=[ticker])

    def fill_missing_values(self):
        """Fill missing values in data frame, in place."""
        self.df.fillna(method='ffill', inplace=True)
        self.df.fillna(method='bfill', inplace=True)

    def normalize(self):
        """Normalize data by first row"""
        return self.df / self.df.ix[0]

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


class Stock(object):
    def __init__(self):
        self.data = {}

    def column(self, name):
        if name not in self.data:
            self.data[name] = Column(name)

        return self.data[name]

    def get_date_range(self, dates):
        m = Stock()
        for name, column in self.data.iteritems():
            m.data[name] = column.get_date_range(dates)
        return m

    def set_baseline(self, ticker):
        for _, column in self.data.iteritems():
            column.set_baseline(ticker)

    def fill_missing_values(self):
        for _, column in self.data.iteritems():
            column.fill_missing_values()

