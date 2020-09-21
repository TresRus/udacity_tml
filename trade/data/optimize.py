import numpy as np
import scipy.optimize as spo
from trade.type import Allocation
from trade.data.process import (Pipe, Portfolio, DailyReturn, Lambda)
from trade.data.process.statistic import (SharpeRatio)


def _sum_one(allocates):
    return np.sum(allocates) - 1.0


def _lists_to_allocations(columns, parts):
    return [Allocation(columns[i], parts[i]) for i in range(len(columns))]


class FitLine(object):
    def __init__(self, error_function):
        self.error_function = error_function

    def run(self, df):
        tickers_number = df.shape[1]
        allocations = np.ones(tickers_number) / tickers_number
        limits = ()
        for x in range(tickers_number):
            limits += ((0.0, 1.0),)

        constr = {'type': 'eq', 'fun': _sum_one}

        result = spo.minimize(self.error_function, allocations, args=(df,),
                              method='SLSQP', bounds=limits,
                              constraints=constr, options={'disp': True})
        return _lists_to_allocations(df.columns, result.x)


class ReversSharpeRatio(object):
    def __call__(self, parts, df):
        return Pipe(
            Portfolio(_lists_to_allocations(df.columns, parts)),
            DailyReturn(),
            SharpeRatio(),
            Lambda(lambda x: x * -1)
        ).process(df)
