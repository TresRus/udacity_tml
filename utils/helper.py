import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import scipy.optimize as spo
import os
import math
import utils
import datetime
import argparse


def symbol_to_path(symbol, base_dir="data", ext="csv"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.{}".format(str(symbol), str(ext)))


class MarketDataParam(object):
    def __init__(self, dates, param):
        self.param = param
        self.df = pd.DataFrame(index=dates)

    def add_snp_baseline(self):
        # SPY is S&P500 ETF and is used as reference stock.
        # It should be always added to dataframe.
        self.add_ticker("SPY")
        # SPY is traded on every day that exchange is open.
        # All the missing dates are not interesting for calculations.
        self.df = self.df.dropna(subset=["SPY"])

    def add_ticker(self, ticker, base_dir="data"):
        if ticker in self.df.columns:
            return

        file_path = symbol_to_path(ticker, base_dir)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
                              usecols=["Date", self.param], na_values=["nan"])
        df_temp = df_temp.rename(columns={self.param: ticker})
        self.df = self.df.join(df_temp)

    def add_tickers(self, tickers, base_dir="data"):
        for ticker in tickers:
            self.add_ticker(ticker)

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

        constr = {'type': 'eq', 'fun': sum_one}

        result = spo.minimize(error_func, init_allocates, args=(self,),
                              method='SLSQP', bounds=limits,
                              constraints=constr, options={'disp': True})
        return result.x


class MarketData(object):
    def __init__(self, dates):
        self.dates = dates
        self.data = {}

    def add_param(self, param):
        if param not in self.data:
            self.data[param] = MarketDataParam(self.dates, param)

        return self.data[param]


def get_snp_data(tickers, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    md = MarketData(dates)
    ac_data = md.add_param("Adj Close")

    ac_data.add_snp_baseline()
    ac_data.add_tickers(tickers)

    return ac_data.df


def get_data(tickers, params, dates, base_dir="data"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    md = MarketData(dates)
    for param in params:
        param_data = md.add_param(param)
        param_data.add_tickers(tickers, base_dir)
    return md.data


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    dr = (df / df.shift(1)) - 1
    dr.ix[0, :] = 0
    return dr


def compute_momentum(df, window):
    dr = (df - df.shift(window))
    dr.ix[0:window, :] = 0
    return dr


def compute_moving_avg(df, window):
    dr = df.rolling(window).mean()
    dr.ix[0:window, :] = df.ix[0:window, :]
    return dr


def compute_exp_moving_avg(df, window):
    dr = df.ewm(span=window).mean()
    dr.ix[0:window, :] = df.ix[0:window, :]
    return dr


def compute_moving_std(df, window):
    dr = df.rolling(window).std()
    dr.ix[0:window, :] = 0
    return dr


def compute_reletive_strength(df, window):
    delta = df.diff()

    up = delta.copy()
    up[up < 0] = 0

    down = delta.copy()
    down[down > 0] = 0

    ru = up.ewm(span=window).mean().abs()
    rd = down.ewm(span=window).mean().abs()

    res = ru / rd
    res.fillna(method='ffill', inplace=True)

    return res


def compute_prediction(df, predict):
    """Compute and return the daily return values."""
    dr = df.shift(-predict)
    return dr


def sharpe_ratio(df, daily_free_risk):
    daily_returns = compute_daily_returns(df)

    return (daily_returns.mean() - daily_free_risk) / \
        daily_returns.std() * math.sqrt(252)


def daily_free_risk():
    return (1.08 ** (1 / 365) - 1.0)


def reverse_sr(allocates, mdp):
    return utils.sharpe_ratio(mdp.portfolio_val(allocates),
                              daily_free_risk()) * -1


def sum_one(allocates):
    return np.sum(allocates) - 1.0


def print_statistic(df, daily_free_risk):
    daily_returns = compute_daily_returns(df)

    print "Cumulative return:"
    print df.ix[-1] - df.ix[0]
    print "Avg. daily return:"
    print daily_returns.mean()
    print "Risk:"
    print daily_returns.std()
    print "Sharpe ratio (year):"
    print sharpe_ratio(df, daily_free_risk)


def print_allocations(allocates, symbols):
    for x in range(len(allocates)):
        print symbols[x], " - ", allocates[x]


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock data with appropriate axis labels."""
    ax = df.plot(title=title, fontsize=8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def plot_to_pdf(
        name,
        dfs,
        title="Stock prices",
        xlabel="Date",
        ylabel="Price"):
    if not os.path.exists('plots'):
        os.makedirs('plots')
    with PdfPages(symbol_to_path(name, 'plots', 'pdf')) as pdf:
        for df in dfs:
            ax = df.plot(title=title, fontsize=8)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            pdf.savefig()
            plt.close()


def plot_hist(df, symbols, bins=20):
    for symbol in symbols:
        df[symbol].hist(bins=bins, label=symbol)
    plt.legend(loc='upper right')
    plt.show()


def count_betas(df, symbols, base):
    res = ()
    for symbol in symbols:
        if symbol == base:
            continue
        df.plot(kind='scatter', x=base, y=symbol)
        b, a = np.polyfit(df[base], df[symbol], 1)
        res = res + (b,)
    return res


def plot_scatter(df, symbols, base):
    for symbol in symbols:
        if symbol == base:
            continue
        df.plot(kind='scatter', x=base, y=symbol)
        b, a = np.polyfit(df[base], df[symbol], 1)
        lgl = utils.LinRegLearner()
        lgl.train(df[base], df[symbol])
        print symbol, lgl.m, b
        plt.plot(df[base], lgl.query(df[base]), '-', color='r')
        plt.show()


def date_arg(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: %s. Should be in forman YYYY-MM-DD (example: 2020-09-05)." % s
        raise argparse.ArgumentTypeError(msg)
