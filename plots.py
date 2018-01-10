import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import utils

def test_run():
    """Function called by Test Run."""
    symbol_list = ["SPY", "GOOG", "AAPL", "XOM"]
    start_date = "2010-12-31"
    end_date = "2011-06-30"
    dates = pd.date_range(start_date, end_date)
    df_data = utils.get_snp_data(symbol_list, dates)
    utils.fill_missing_values(df_data)

    # utils.plot_data(df_data)

    daily_returns = utils.compute_daily_returns(df_data)
    # unitls.plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # utils.plot_hist(daily_returns, symbol_list)
    # daily_returns.hist(bins=20)
    # plt.show()

    utils.plot_scatter(daily_returns, symbol_list, 'SPY')


if __name__ == "__main__":
    test_run()

