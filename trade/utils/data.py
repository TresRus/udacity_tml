import os
import numpy as np
import pandas as pd
import scipy.optimize as spo
from enum import Enum


def _sum_one(allocates):
    return np.sum(allocates) - 1.0


class Reader(object):
    def read(self, ticker, columns):
        raise NotImplementedError


class CsvReader(Reader):
    def __init__(self, root="data"):
        self.root = root

    def _ticker_cvs_path(self, ticker):
        return os.path.join(self.root, "{}.csv".format(str(ticker)))

    def read(self, ticker, columns):
        if Column.Name.DATE not in columns:
            columns += [Column.Name.DATE]

        file_path = self._ticker_cvs_path(ticker)
        return pd.read_csv(
            file_path,
            parse_dates=True,
            index_col=Column.Name.DATE,
            usecols=columns,
            na_values=["nan"])


class Column(object):
    class Name(Enum):
        DATE = "Date"
        ADJCLOSE = "Adj Close"
        CLOSE = "Close"
        HIGH = "High"
        LOW = "Low"
        OPEN = "Open"
        VOLUME = "Volume"

    def __init__(self, column, reader):
        self.reader = reader
        self.column = column
        self.df = pd.DataFrame()

    def get_date_range(self, dates):
        df = pd.DataFrame(index=dates)
        df = df.join(self.df, how="inner")
        return df

    def set_baseline(self, ticker):
        # SPY is S&P500 ETF and is used as reference stock.
        # It should be always added to dataframe.
        self.load_ticker(ticker)
        # SPY is traded on every day that exchange is open.
        # All the missing dates are not interesting for calculations.
        self.df = self.df.dropna(subset=[ticker])

    def load_ticker(self, ticker):
        if ticker in self.df.columns:
            return

        df_temp = self.reader.read(ticker, [self.column])
        df_temp = df_temp.rename(columns={self.column: ticker})
        self.df = self.df.join(df_temp, how="outer")

    def load_tickers(self, tickers):
        for ticker in tickers:
            self.load_ticker(ticker)

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


class Market(object):
    def __init__(self, reader):
        self.reader = reader
        self.data = {}

    def column(self, name):
        if name not in self.data:
            self.data[name] = Column(name, self.reader)

        return self.data[name]

    def load(self, tickers, columns):
        for column in columns:
            cd = self.column(column)
            cd.load_tickers(tickers)

    def set_baseline(self, ticker):
        for _, column in self.data.iteritems():
            column.set_baseline(ticker)

    def fill_missing_values(self):
        for _, column in self.data.iteritems():
            column.fill_missing_values()
