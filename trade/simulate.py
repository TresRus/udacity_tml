import pandas as pd
from trade.type import Allocation, AllocationSet
from trade.data import process


class Strategy(object):
    def apply(self, df):
        raise NotImplementedError

    def holdings(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

class HoldMoney(Strategy):
    def __init__(self, total):
        self.total = total

    def apply(self, df):
        pass

    def holdings(self):
        return (self.total, AllocationSet())

    def value(self):
        return self.total


class HoldAllocation(Strategy):
    def __init__(self, total, allocations):
        self.cash = total
        self.holding_value = 0
        self.allocations = allocations
        self.allocation_set = AllocationSet([])
        self.init = False

    def apply(self, df):
        if not self.init:
            self.rebalance(df)
            self.init = True
        self.update_value(df)

    def rebalance(self, df):
        total = self.value()
        self.allocation_set = process.PortfolioSet(
            self.allocations, total
        ).process(df)
        self.update_value(df)
        self.cash = total - self.holding_value

    def holdings(self):
        return (self.cash, self.allocation_set)

    def update_value(self, df):
        self.holding_value = process.PortfolioSetValue(
            self.allocation_set
        ).process(df[-1:]).iloc[0]['Value']

    def value(self):
        return self.cash + self.holding_value

class OptimizerAllocation(Strategy):
    def __init__(self, total, optimizer):
        self.cash = total
        self.holding_value = 0
        self.allocation_set = AllocationSet([])
        self.optimizer = optimizer
        self.init = False

    def apply(self, df):
        if not self.init:
            self.rebalance(df)
            self.init = True
        self.update_value(df)

    def rebalance(self, df):
        total = self.value()
        allocations = self.optimizer.run(df)
        self.allocation_set = process.PortfolioSet(
            allocations, total
        ).process(df)
        self.update_value(df)
        self.cash = total - self.holding_value

    def holdings(self):
        return (self.cash, self.allocation_set)

    def update_value(self, df):
        self.holding_value = process.PortfolioSetValue(
            self.allocation_set
        ).process(df[-1:]).iloc[0]['Value']

    def value(self):
        return self.cash + self.holding_value


class MonthlyRebalance(Strategy):
    def __init__(self, strategy):
        self.strategy = strategy
        self.start_data = None
        self.init = False

    def apply(self, df):
        if not self.init:
            self.next_balance = df.iloc[-1].name + pd.DateOffset(months=1)
            self.init = True

        if df.iloc[-1].name > self.next_balance:
            self.strategy.rebalance(df)
            self.next_balance = df.iloc[-1].name + pd.DateOffset(months=1)

        return self.strategy.apply(df)

    def holdings(self):
        return self.strategy.holdings()

    def value(self):
        return self.strategy.value()


class Simulator(object):
    def __init__(self, df, window):
        self.df = df
        self.window = window

    def run(self, strategy, column):
        result = pd.DataFrame(columns=[column], index=self.df[self.window:].index)
        for i in range(0, self.df.shape[0] - self.window):
            strategy.apply(self.df[i:self.window + i])
            result.loc[self.df.iloc[self.window + i].name] = [strategy.value()]
        return result
        
