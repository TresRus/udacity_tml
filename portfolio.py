import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import (statistic, plot)
import trade.type


def portfolio(allocations, baseline, start, end):
    """Function called by Test Run."""
    tickers = [allocation.ticker for allocation in allocations]
    dates = pd.date_range(start, end)

    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates),
        process.Normalize(),
        process.Split(
            process.Portfolio(allocations),
            process.Pass()
        ),
        process.Merge()
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))

    statistic.Print().process(data)
    plot.Plot(plot.Graph()).process(data)


def run():
    parser = argparse.ArgumentParser(description='Portfolio statistic.')
    parser.add_argument(
        'allocations',
        metavar='T',
        type=trade.type.Allocation.argparse,
        nargs='+',
        help='ticker and the part to include in portfolio')
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    args = parser.parse_args()

    portfolio(args.allocations, args.baseline, args.start, args.end)


if __name__ == "__main__":
    run()
