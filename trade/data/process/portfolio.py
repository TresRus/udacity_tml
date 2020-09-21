from .allocate import Allocate
from .filter import Filter
from .utils import Pipe, Lambda
from .sum import Sum


class Portfolio(object):
    def __init__(self, allocations, total_cost=1.0):
        self.tickers = [allocation.ticker for allocation in allocations]
        self.parts = [allocation.number for allocation in allocations]
        total = sum(self.parts)
        self.parts = [float(part) / total for part in self.parts]
        self.total_cost = total_cost
        self.processor = Pipe(
            Filter(
                self.tickers), Allocate(
                self.parts), Lambda(
                lambda df: df * self.total_cost), Sum("Portfolio"))

    def process(self, df):
        for ticker in self.tickers:
            if ticker not in df.columns:
                raise ValueError(
                    "Ticker {} is not presented in dataframe".format(ticker))
        return self.processor.process(df)
