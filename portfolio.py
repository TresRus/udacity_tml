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

    print "Cumulative:"
    print str(process.statistic.Cumulative().process(stock))
    print "Average:"
    print str(process.statistic.Average().process(daily_return))
    print "Risk:"
    print str(process.statistic.Risk().process(daily_return))
    print "Sharpe ratio (year):"
    print str(process.statistic.SharpeRatio().process(daily_return))
    print "Alpha to SPY:"
    print str(process.statistic.Alpha('SPY').process(daily_return))
    print "Beta to SPY:"
    print str(process.statistic.Beta('SPY').process(daily_return))


if __name__ == "__main__":
    test_run()
