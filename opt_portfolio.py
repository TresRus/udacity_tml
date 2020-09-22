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
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))
    allocations_sr = trade.data.optimize.FitLine(
        trade.data.optimize.ReversSharpeRatio()).run(data)

    print("Risk and return optimized")
    for allocation in allocations_sr:
        print(allocation)

    allocations_mm = trade.data.optimize.FitLine(
        trade.data.optimize.MinimalMarket(baseline)).run(data)

    print("Minimal market influence")
    for allocation in allocations_mm:
        print(allocation)

    data = process.Pipe(
        process.Split(
            process.Normalize(),
            process.Pipe(
                process.Portfolio(allocations_sr),
                process.TickerSuffix("_sr")
            ),
            process.Pipe(
                process.Portfolio(allocations_mm),
                process.TickerSuffix("_mm")
            )
        ),
        process.Merge()
    ).process(data)

    process.statistic.Print().process(data)
    process.Pipe(
        process.Filter([baseline, 'Portfolio_sr', 'Portfolio_mm']),
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
