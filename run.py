"""Fill missing values"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
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


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock data with appropriate axis labels."""
    ax = df.plot(title=title, fontsize=8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    return (df / df.shift(1)) - 1


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
        #c = np.polyfit(df[base], df[symbol], 1)
        #plt.plot(df[base], c[0] * df[base] + c[1], '-', color='r')
        plt.show()


def test_run():
    """Function called by Test Run."""
    symbol_list = ["SPY", "GOOG", "AAPL", "XOM"]
    start_date = "2010-12-31"
    end_date = "2011-12-31"
    dates = pd.date_range(start_date, end_date)
    df_data = get_data(symbol_list, dates)
    fill_missing_values(df_data)

    plot_data(df_data)

    daily_returns = compute_daily_returns(df_data)
    #plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # plot_hist(daily_returns, symbol_list)
    #daily_returns.hist(bins=20)
    #plt.show()

    plot_scatter(daily_returns, symbol_list, 'SPY')


if __name__ == "__main__":
    test_run()

