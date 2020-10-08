import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import (statistic, plot)
import trade.type


def portfolio(allocations, baseline, start, end, stat):
    tickers = [allocation.ticker for allocation in allocations]
    dates = pd.date_range(start, end)
    
    for allocation in allocations:
        print(allocation)

    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates)
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))

    port_data = process.PortfolioSetValue(
        trade.type.AllocationSet(allocations)
    ).process(data)

    if stat:
        statistic.Print().process(port_data)
    plot.Plot(plot.Graph()).process(port_data)


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
    parser.add_argument('--stat', action='store_true',
                        help="Show statistics")
    args = parser.parse_args()

    portfolio(args.allocations, args.baseline, args.start, args.end, args.stat)


if __name__ == "__main__":
    run()
