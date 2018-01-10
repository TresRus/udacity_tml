import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import utils

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_snp_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df_final = pd.DataFrame(index=dates)
    if "SPY" not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, "SPY")

    for symbol in symbols:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
            usecols=["Date", "Adj Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        df_final = df_final.join(df_temp)
        if symbol == "SPY":  # drop dates SPY did not trade
            df_final = df_final.dropna(subset=["SPY"])

    return df_final

def get_data(symbols, dates, base_dir="data"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df_final = pd.DataFrame(index=dates)

    for symbol in symbols:
        file_path = symbol_to_path(symbol, base_dir)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
            usecols=["Date", "Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Close": symbol})
        df_final = df_final.join(df_temp)

    return df_final


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
    dr.ix[0:window, :] = 0
    return dr


def normolize(df):
    """Normalize data by first row"""
    return df / df.ix[0]


def portfolio_val(df, allocates, cost=1.0):
    port = normolize(df) * allocates
    port = port * cost

    dr = port.sum(axis=1)
    dr.name = "Portfolio"
    return dr.to_frame()


def sharpe_ratio(df, daily_free_risk):
    daily_returns = compute_daily_returns(df)

    return (daily_returns.mean() - daily_free_risk) / daily_returns.std() * math.sqrt(252)


def daily_free_risk():
    return (1.08 ** (1 / 365) - 1.0)


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


def plot_hist(df, symbols, bins=20):
    for symbol in symbols:
        df[symbol].hist(bins=bins, label=symbol)
    plt.legend(loc='upper right')
    plt.show()


def plot_scatter(df, symbols, base):
    for symbol in symbols:
        if symbol == base:
            continue
        df.plot(kind='scatter', x=base, y=symbol)
        lgl = utils.LinRegLearner()
        lgl.train(df[base], df[symbol])
        plt.plot(df[base], lgl.query(df[base]), '-', color='r')
        plt.show()

