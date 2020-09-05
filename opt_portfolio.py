import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as spo
import utils


def reverse_sr(allocates, df):
    return utils.sharpe_ratio(utils.portfolio_val(df, allocates),
                              utils.daily_free_risk()) * -1


def sum_one(allocates):
    return np.sum(allocates) - 1.0


def fit_line(df, error_func):
    column_num = df.shape[1]
    init_allocates = np.ones(column_num) / column_num
    limits = ()
    for x in range(column_num):
        limits += ((0.0, 1.0),)

    constr = {'type': 'eq', 'fun': sum_one}

    result = spo.minimize(error_func, init_allocates, args=(df,),
                          method='SLSQP', bounds=limits,
                          constraints=constr, options={'disp': True})
    return result.x


def optimize(tickers, start, end):
    dates = pd.date_range(start, end)
    df_data = utils.get_snp_data(tickers, dates)
    utils.fill_missing_values(df_data)

    norm = utils.normalize(df_data)
    utils.print_statistic(norm, utils.daily_free_risk())

    market = utils.normalize(utils.get_snp_data(["SPY"], dates))

    result_allocates = fit_line(df_data, reverse_sr)
    utils.print_allocations(result_allocates, tickers)

    portfolio = utils.portfolio_val(df_data, result_allocates)
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
