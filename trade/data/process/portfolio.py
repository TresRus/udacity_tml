import numpy as np
import pandas as pd
from .allocate import Allocate
from .filter import Filter
from .utils import Pipe, Lambda
from .returns import CumulativeReturn, ReverseCumulativeReturn
from .sum import Sum
from .tail import Tail
from trade.type import Allocation, AllocationSet


class Portfolio(object):
    def __init__(self, allocations, total_cost=1.0):
        self.tickers = [allocation.ticker for allocation in allocations]
        self.parts = [allocation.number for allocation in allocations]
        total = np.sum(np.abs(self.parts))
        self.parts = [float(part) / total for part in self.parts]
        self.total_cost = total_cost
        self.processor = Pipe(
            Filter(self.tickers),
            CumulativeReturn(),
            Allocate(self.parts),
            Sum("Portfolio"),
            ReverseCumulativeReturn(),
            Lambda(lambda df: df * self.total_cost))

    def process(self, df):
        for ticker in self.tickers:
            if ticker not in df.columns:
                raise ValueError(
                    "Ticker {} is not presented in dataframe".format(ticker))
        return self.processor.process(df)

class PortfolioSet(object):
    def __init__(self, allocations, total_cost=1.0):
        self.tickers = [allocation.ticker for allocation in allocations]
        parts = [allocation.number for allocation in allocations]
        total = np.sum(np.abs(parts))
        parts = [float(part) / total for part in parts]
        self.costs = pd.Series([part * total_cost for part in parts], index=self.tickers)
        self.processor = Pipe(
            Filter(self.tickers),
            Lambda(lambda df: self.costs / df.iloc[-1]),
            Lambda(lambda s: AllocationSet(
                    [Allocation(ticker, number) for ticker, number in s.items()]
                  ))
        )

    def process(self, df):
        for ticker in self.tickers:
            if ticker not in df.columns:
                raise ValueError(
                    "Ticker {} is not presented in dataframe".format(ticker))
        return self.processor.process(df)
