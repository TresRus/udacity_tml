import json
import datetime
import pandas as pd

from trade.data import (ColumnName, reader, process)
from trade.data.process import plot
import trade.data.optimize

def optimize(tickers, baseline, start, end, cost, short, stat, json_path):
    if baseline not in tickers:
        tickers += [baseline]

    dates = pd.date_range(start, end)
    data = process.Pipe(
        process.Baseline(baseline),
        process.FillMissing(),
        process.Range(dates),
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))
    allocations = trade.data.optimize.FitLine(
        trade.data.optimize.ReversSharpeRatio(), short).run(data)

    allocation_set = process.PortfolioSet(allocations, cost).process(data)
    print("Risk and return optimized")
    print(allocation_set)
    value = process.PortfolioSetValue(
        allocation_set
    ).process(data[-1:]).iloc[0]['Value']
    print("Portfolio value: ", value)
    print("Parts")
    for allocation in allocations:
        print(allocation)

    if json_path:
        with open(json_path, "w") as json_file:
            json.dump(allocation_set.data, json_file, indent=4)

    data = process.Pipe(
        process.Split(
            process.Normalize(),
            process.Portfolio(allocation_set.get_list()),
        ),
        process.Merge()
    ).process(data)

    if stat:
        process.statistic.Print().process(data)
    process.Pipe(
        process.Filter([baseline, 'Portfolio']),
        plot.Plot(plot.Graph())
    ).process(data)


def value(allocation_set, date=None):
    date_filter = process.Tail(1)
    if date is not None:
        date_filter = process.Range(pd.date_range(date, date))
    tickers = allocation_set.data.keys()

    data = process.Pipe(
        process.FillMissing(),
        date_filter,
    ).process(reader.CsvReader().read_column(tickers, ColumnName.ADJCLOSE))

    value = process.PortfolioSetValue(
        allocation_set
    ).process(data).iloc[0]['Value']
    print("Portfolio value: ", value)
    return value


