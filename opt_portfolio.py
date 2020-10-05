import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import plot
import trade.type
import trade.data.optimize


def optimize(tickers, baseline, start, end, cost, short, stat):
    if baseline not in tickers:
        tickers += [baseline]

    dates = pd.date_range(start, end)
    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates),
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))
    allocations_sr = trade.data.optimize.FitLine(
        trade.data.optimize.ReversSharpeRatio(), short).run(data)

    print("Risk and return optimized")
    print(process.PortfolioSet(allocations_sr, cost).process(data))
    print("Parts")
    for allocation in allocations_sr:
        print(allocation)


    allocations_mm = trade.data.optimize.FitLine(
        trade.data.optimize.MinimalMarket(baseline), short).run(data)

    print("Minimal market influence")
    print(process.PortfolioSet(allocations_mm, cost).process(data))
    print("Parts")
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

    if stat:
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
    parser.add_argument('-c', '--cost', default=1, type=int,
                        help="Total portfolio cost")
    parser.add_argument('--short', action='store_true',
                        help="Allow shorting")
    parser.add_argument('--stat', action='store_true',
                        help="Show statistics")
    args = parser.parse_args()

    optimize(args.tickers, args.baseline, args.start, args.end, args.cost, args.short, args.stat)


if __name__ == "__main__":
    run()
