import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import plot
from trade.simulate import (Simulator, HoldMoney, HoldAllocation,
                            MonthlyRebalance, OptimizerAllocation)
import trade.type
import trade.data.optimize
from trade.type import Allocation
import trade.data.optimize


def simulate(tickers, baseline, start, end, cost):
    if baseline not in tickers:
        tickers += [baseline]

    dates = pd.date_range(start, end)
    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates),
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))

    simulator = Simulator(data, 252)
    allocations = []
    for ticker in tickers:
        allocations += [Allocation(ticker, 1)]
    sim = process.Merge().process(
        # simulator.run(HoldMoney(cost), "Hold money"),
        simulator.run(
            HoldAllocation(cost, [Allocation(baseline, 1)]),
            "Hold only baseline"),
        simulator.run(
            MonthlyRebalance(
                HoldAllocation(cost, allocations)),
            "Hold equal allocation + mrb"),
        simulator.run(
            MonthlyRebalance(
                OptimizerAllocation(cost,
                    trade.data.optimize.FitLine(
                        trade.data.optimize.ReversSharpeRatio(), False))),
            "Optimizer allocation + mrb")
    )
    print(sim)
    plot.Plot(plot.Graph()).process(sim)


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
    args = parser.parse_args()

    simulate(args.tickers, args.baseline, args.start, args.end, args.cost)


if __name__ == "__main__":
    run()
