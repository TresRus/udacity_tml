import math
import pandas as pd
from trade import utils
from .daily_return import DailyReturn


class Cumulative(object):
    def process(self, df):
        return df.iloc[-1] - df.iloc[0]


class Average(object):
    def process(self, df):
        return df.mean()


class Risk(object):
    def process(self, df):
        return df.std()


class SharpeRatio(object):
    def __init__(self, risk_free=0.00, days=252):
        self.daily_free_risk = ((1.0 + risk_free) ** (1 / 252) - 1.0)
        self.days = 252

    def process(self, df):
        return (df.mean() - self.daily_free_risk) / \
            df.std() * math.sqrt(self.days)


class Alpha(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def process(self, df):
        if self.ticker not in df.columns:
            raise ValueError(
                "No {} ticker in dataframe".format(self.ticker))

        data = []
        learner = utils.LinRegLearner()
        for ticker in df.columns:
            learner.train(df[self.ticker], df[ticker])
            data.append(learner.b)

        return pd.Series(data, index=df.columns.tolist())


class Beta(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def process(self, df):
        if self.ticker not in df.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.ticker, column.name))

        data = []
        learner = utils.LinRegLearner()
        for ticker in df.columns:
            learner.train(df[self.ticker], df[ticker])
            data.append(learner.m)

        return pd.Series(data, index=df.columns.tolist())


class Correlation(object):
    def process(self, df):
        return df.corr(method='pearson')


class Print(object):
    def process(self, stock):
        daily_return = DailyReturn().process(stock)

        print("Cumulative:")
        print(str(Cumulative().process(stock)))
        print("Average:")
        print(str(Average().process(daily_return)))
        print("Risk:")
        print(str(Risk().process(daily_return)))
        print("Sharpe ratio (year):")
        print(str(SharpeRatio().process(daily_return)))
        print("Alpha to SPY:")
        print(str(Alpha('SPY').process(daily_return)))
        print("Beta to SPY:")
        print(str(Beta('SPY').process(daily_return)))
        print("Correlation:")
        print(str(Correlation().process(daily_return)))
