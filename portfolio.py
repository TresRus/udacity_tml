import os
import argparse
import pandas as pd
from trade import utils
from trade.data import (Column, reader, process)


def test_run():
    """Function called by Test Run."""
    baseline = "SPY"
    tickers = ["SPY", "GOOG", "AAPL", "XOM"]
    allocates = [0.3, 0.4, 0.1, 0.1]
    start_date = "2010-12-31"
    end_date = "2017-12-01"
    dates = pd.date_range(start_date, end_date)

    stock = process.ProcessLine([process.Baseline(baseline), process.FillMissing(), process.Range(
        dates)]).process(reader.CsvReader().read_stock(tickers, [Column.Name.ADJCLOSE]))
    daily_return = process.DailyReturn().process(stock)

    print process.Statistic().process(daily_return)

    utils.print_statistic(stock.column(Column.Name.ADJCLOSE).df, daily_return.column(
        Column.Name.ADJCLOSE).df, (1.08 ** (1 / 365) - 1.0))


if __name__ == "__main__":
    test_run()
