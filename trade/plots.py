import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils


def plot_tickers(tickers, start, end):
    m = utils.data.Market(utils.data.CsvReader())
    m.load(tickers, [utils.data.Column.Name.ADJCLOSE])
    m.fill_missing_values()
    
    dates = pd.date_range(start, end)
    dates_m = m.get_date_range(dates)

    ac_data = dates_m.column(utils.data.Column.Name.ADJCLOSE)
    utils.plot_data(ac_data.normalize())

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
