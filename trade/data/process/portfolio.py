from trade.data import Column
from trade.data.process import (ProcessLine, Filter, Allocate, Multiply, Sum)


class Portfolio(object):
    def __init__(self, allocations, total_cost=1.0):
        self.tickers = [ allocation.ticker for allocation in allocations ]
        self.parts = [ allocation.number for allocation in allocations ]
        total = sum( self.parts )
        self.parts = [ float(part) / total for part in self.parts ]
        self.total_cost = total_cost

    def process(self, stock):
        return ProcessLine([Filter(self.tickers), Allocate(self.parts), Multiply(self.total_cost), Sum("Portfolio")]).process(stock)
