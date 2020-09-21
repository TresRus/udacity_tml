import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import plot
import trade.type
import trade.data.optimize


def optimize(tickers, baseline, start, end):
    if baseline not in tickers:
        tickers += [baseline]

    dates = pd.date_range(start, end)
    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates),
        process.Normalize(),
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))
    allocations = trade.data.optimize.FitLine(
        trade.data.optimize.ReversSharpeRatio()).run(data)

    for allocation in allocations:
        print(allocation)

    data = process.Pipe(
        process.Split(
            process.Pass(),
            process.Portfolio(allocations)
        ),
        process.Merge()
    ).process(data)

    process.statistic.Print().process(data)
    process.Pipe(
        process.Filter([baseline, 'Portfolio']),
        plot.Plot(plot.Graph())
    ).process(data)


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    args = parser.parse_args()

    optimize(args.tickers, args.baseline, args.start, args.end)


if __name__ == "__main__":
    run()
