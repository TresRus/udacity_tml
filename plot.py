import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from trade import utils
from trade.data import (storage, reader, process)


def plot_tickers(tickers, start, end):
    dates = pd.date_range(start, end)
    stock = process.ProcessLine([process.FillMissing(), process.Range(dates)]).process(
        reader.CsvReader().read_stock(tickers, [storage.Column.Name.ADJCLOSE]))

    utils.plot_data(stock.column(storage.Column.Name.ADJCLOSE).normalize())

    # daily_returns = utils.compute_daily_returns(ac_data.df)
    # unitls.plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # utils.plot_hist(daily_returns, symbol_list)
    # daily_returns.hist(bins=20)
    # plt.show()

    # utils.plot_scatter(daily_returns, tickers, 'SPY')


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-s', '--start', required=True, type=utils.date_arg,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=utils.date_arg,
                        help="Evaluation end date")
    args = parser.parse_args()

    plot_tickers(args.tickers, args.start, args.end)


if __name__ == "__main__":
    run()
