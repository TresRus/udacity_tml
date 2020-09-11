import os
import argparse
import pandas as pd
from trade import utils
from trade.data import (Column, reader, process)
import trade.type
import trade.data.optimize


def optimize(tickers, baseline, start, end):
    if baseline not in tickers:
        tickers += [baseline]

    dates = pd.date_range(start, end)
    stock = process.ProcessLine([process.Baseline(baseline), process.FillMissing(), process.Range(
        dates)]).process(reader.CsvReader().read_stock(tickers, [Column.Name.ADJCLOSE]))

    stock = process.Normalize().process(stock)

    allocations = trade.data.optimize.FitLine(trade.data.optimize.ReversSharpeRatio()).run(stock.column(Column.Name.ADJCLOSE))

    for allocation in allocations:
        print allocation

    portfolio = process.Portfolio(allocations).process(stock)
    stock = process.Merger().process([stock, portfolio])

    process.statistic.Print().process(stock)
    process.ProcessLine([process.Filter([baseline, 'Portfolio']), process.Plot(process.plot.Graph())]).process(stock)

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
