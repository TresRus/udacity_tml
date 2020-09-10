import math
import pandas as pd
import column_base
from trade import utils
from trade.data import Column


class Cumulative(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.ix[-1] - column.data.ix[0]
        return result_column

class Average(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.mean()
        return result_column

class Risk(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.std()
        return result_column

class SharpeRatio(column_base.ColumnBase):
    def __init__(self, risk_free=0.08, days=252):
        self.daily_free_risk = ((1.0 + risk_free) ** (1 / 365) - 1.0)
        self.days = 252

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = (column.data.mean() - self.daily_free_risk) / column.data.std() * math.sqrt(self.days)
        return result_column

class Alpha(column_base.ColumnBase):
    def __init__(self, ticker):
        self.ticker = ticker

    def process_column(self, column):
        if self.ticker not in column.data.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.ticker, column.name))

        result_column = Column(column.name)
        data = []
        learner = utils.LinRegLearner()
        for ticker in column.data.columns:
            learner.train(column.data[self.ticker], column.data[ticker])
            data.append(learner.b)

        result_column = pd.Series(data, index=column.data.columns.tolist())
        return result_column

class Beta(column_base.ColumnBase):
    def __init__(self, ticker):
        self.ticker = ticker

    def process_column(self, column):
        if self.ticker not in column.data.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.ticker, column.name))

        result_column = Column(column.name)
        data = []
        learner = utils.LinRegLearner()
        for ticker in column.data.columns:
            learner.train(column.data[self.ticker], column.data[ticker])
            data.append(learner.m)

        result_column = pd.Series(data, index=column.data.columns.tolist())
        return result_column
