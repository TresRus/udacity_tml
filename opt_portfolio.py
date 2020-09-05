import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as spo
import utils

def reverse_sr(allocates, df):
    return utils.sharpe_ratio(utils.portfolio_val(df, allocates), utils.daily_free_risk()) * -1;

def sum_one(allocates):
    return np.sum(allocates) - 1.0

def fit_line(df, error_func):
    column_num = df.shape[1]
    init_allocates = np.ones(column_num) / column_num

    limits = ()
    for x in range(column_num):
        limits += ((0.0, 1.0),)

    constr = {'type':'eq', 'fun':sum_one}

    result = spo.minimize(error_func, init_allocates, args=(df,), method='SLSQP', bounds=limits, constraints=constr, options={'disp': True})
    return result.x

def test_run():
    """Function called by Test Run."""
    symbol_list = ["SPY", "GOOG", "AAPL", "XOM", "GLD" ]
    start_date = "2017-01-01"
    end_date = "2019-01-01"
    dates = pd.date_range(start_date, end_date)
    df_data = utils.get_snp_data(symbol_list, dates)
    utils.fill_missing_values(df_data)

    norm = utils.normalize(df_data)
    utils.print_statistic(norm, utils.daily_free_risk())

    market = utils.normalize(utils.get_snp_data(["SPY"], dates))

    result_allocates = fit_line(df_data, reverse_sr)
    utils.print_allocations(result_allocates, symbol_list)

    portfolio = utils.portfolio_val(df_data, result_allocates)
    market = market.join(portfolio)

    utils.print_statistic(market, utils.daily_free_risk())

    utils.plot_data(market)


if __name__ == "__main__":
    test_run()

