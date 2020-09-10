import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from trade import utils
from trade.data import (Column, reader, process)


def plot_tickers(tickers, baseline, start, end):
    dates = pd.date_range(start, end)
    stock = process.ProcessLine([process.FillMissing(), process.Range(dates)]).process(
        reader.CsvReader().read_stock(tickers + [baseline], [Column.Name.ADJCLOSE]))
    normalized_stock = process.Normalize().process(stock)
    daily_return = process.DailyReturn().process(stock)

    root_dir = os.path.dirname(os.path.realpath(__file__))
    plot_dir = os.path.join(root_dir, "plots")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plot_path = os.path.join(plot_dir, "Market.pdf")
    process.PdfPlot([process.StockPlotter([process.plot.Graph()],
                                          normalized_stock),
                     process.StockPlotter([process.plot.Histogram(baseline=baseline)],
                                          daily_return)],
                    plot_path).plot()

    for ticker in tickers:
        plot_path = os.path.join(plot_dir, "{}.pdf".format(ticker))

        tstock = process.Filter([ticker]).process(stock)
        tdr = process.Filter([ticker]).process(daily_return)
        btdr = process.Filter([ticker, baseline]).process(daily_return)

        process.PdfPlot([process.StockPlotter([process.plot.Graph(title="Stock")],
                                              tstock),
                         process.StockPlotter([process.plot.Graph(title="Daily returns",
                                                                  ylabel="Return"),
                                               process.plot.Histogram()],
                                              tdr),
                         process.StockPlotter([process.plot.Scatter(baseline)],
                                              btdr)],
                        plot_path).plot()


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-s', '--start', required=True, type=utils.date_arg,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=utils.date_arg,
                        help="Evaluation end date")
    args = parser.parse_args()

    plot_tickers(args.tickers, args.baseline, args.start, args.end)


if __name__ == "__main__":
    run()
