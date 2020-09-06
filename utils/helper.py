import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os
import math
import utils
import argparse
import datetime


def symbol_to_path(symbol, base_dir="data", ext="csv"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.{}".format(str(symbol), str(ext)))


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
        xlabel="Date",
        ylabel="Price"):
    if not os.path.exists('plots'):
        os.makedirs('plots')
    with PdfPages(symbol_to_path(name, 'plots', 'pdf')) as pdf:
        for name, df in dfs:
            ax = df.plot(title=name, fontsize=8)
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
