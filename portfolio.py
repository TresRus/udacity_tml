import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import utils

def test_run():
    """Function called by Test Run."""
    symbol_list = ["SPY", "GOOG", "AAPL", "XOM"]
    allocates = [0.4, 0.4, 0.1, 0.1]
    start_date = "2010-12-31"
    end_date = "2011-12-31"
    dates = pd.date_range(start_date, end_date)
    df_data = utils.get_data(symbol_list, dates)
    utils.fill_missing_values(df_data)

    portfolio = utils.portfolio_val(df_data, allocates, 10000)

    utils.print_statistic(portfolio, (1.08 ** (1 / 365) - 1.0))
    utils.print_statistic(df_data, (1.08 ** (1 / 365) - 1.0))


if __name__ == "__main__":
    test_run()

