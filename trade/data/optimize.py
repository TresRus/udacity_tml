import numpy as np
import scipy.optimize as spo
from trade.type import Allocation
from trade.data.process import (Pipe, Portfolio, DailyReturn, Lambda, Split, Merge, Filter, TickerSuffix, Sum)
from trade.data.process.statistic import (SharpeRatio, Alpha, Beta)


def _sum_one(allocates):
    return np.sum(np.abs(allocates)) - 1.0


def _lists_to_allocations(columns, parts):
    return [Allocation(columns[i], parts[i]) for i in range(len(columns))]


class FitLine(object):
    def __init__(self, error_function, short=False):
        self.error_function = error_function
        self.short = short

    def run(self, df):
        tickers_number = df.shape[1]
        allocations = np.ones(tickers_number) / tickers_number
        limits = ()
        for x in range(tickers_number):
            if self.short:
                limits += ((-1.0, 1.0),)
            else:
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

class MinimalMarket(object):
    def __init__(self, baseline):
        self.baseline = baseline

    def __call__(self, parts, df):
        return Pipe(
            Split(
                Filter([self.baseline]),
                Portfolio(_lists_to_allocations(df.columns, parts))
            ),
            Merge(),
            DailyReturn(),
            Split(
                Pipe(
                    Beta(self.baseline),
                    Lambda(lambda x: (x * 100) ** 2),
                    Lambda(lambda x: x.loc["Portfolio"])
                ),
                Pipe(
                    Alpha(self.baseline),
                    Lambda(lambda x: (x * -1000) ** 3),
                    Lambda(lambda x: x.loc["Portfolio"])
                )
            ),
            Lambda(lambda x: x[0] + x[1])
        ).process(df)
