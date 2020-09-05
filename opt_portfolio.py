import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils


def optimize(tickers, start, end):
    dates = pd.date_range(start, end)
    md = utils.MarketData(dates)
    ac_data = md.param("Adj Close")

    ac_data.add_snp_baseline()
    ac_data.add_tickers(tickers)
    ac_data.fill_missing_values()

    norm = ac_data.normalize()
    utils.print_statistic(norm, utils.daily_free_risk())

    print norm.head()

    market = norm[['SPY']]

    result_allocates = ac_data.fit_line(utils.reverse_sr)
    utils.print_allocations(result_allocates, ac_data.df.columns)

    portfolio = ac_data.portfolio_val(result_allocates)
    market = market.join(portfolio)

    utils.print_statistic(market, utils.daily_free_risk())

    utils.plot_data(market)


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-s', '--start', required=True, type=utils.date_arg,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=utils.date_arg,
                        help="Evaluation end date")
    args = parser.parse_args()

    optimize(args.tickers, args.start, args.end)


if __name__ == "__main__":
    run()
