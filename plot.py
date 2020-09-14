import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from trade.data import (Column, reader, process)
import trade.type


def plot_tickers(tickers, baseline, window, start, end):
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

        tstock_ma = process.ProcessLine([process.TickerSuffix(
            "_mov_avg({})".format(window)), process.MovingAverage(window)]).process(tstock)
        tstock_mah = process.ProcessLine([process.TickerSuffix("_mov_avg({})".format(
            window / 2)), process.MovingAverage(window / 2)]).process(tstock)
        tstock_maq = process.ProcessLine([process.TickerSuffix("_mov_avg({})".format(
            window / 4)), process.MovingAverage(window / 4)]).process(tstock)
        tstock_ubb = process.ProcessLine([process.TickerSuffix("_upper_bb({})".format(
            window)), process.UpperBollingerBand(window)]).process(tstock)
        tstock_lbb = process.ProcessLine([process.TickerSuffix("_lower_bb({})".format(
            window)), process.LowerBollingerBand(window)]).process(tstock)

        tstock_emad = process.Emad(window).process(tstock)
        tstock_macd = process.ProcessLine([process.TickerSuffix("_macd({})".format(
            window)), process.ExponentialMovingAverage(window / 3)]).process(tstock_emad)
        tstock_emad = process.TickerSuffix(
            "_emad({})".format(window)).process(tstock_emad)

        stock_bands = process.Tail(
            window *
            3).process(
            process.Merger().process(
                [
                    tstock,
                    tstock_ma,
                    tstock_ubb,
                    tstock_lbb]))
        stock_avgs = process.Tail(
            window * 3).process(process.Merger().process([tstock, tstock_mah, tstock_maq]))
        stock_macd = process.Tail(
            window * 3).process(process.Merger().process([tstock_emad, tstock_macd]))
        short_tdr = process.Tail(window * 3).process(tdr)
        stock_rsi = process.ProcessLine([process.TickerSuffix("_rsi({})".format(
            window)), process.RelativeStrengthIndex(window), process.Tail(window * 3)]).process(tstock)

        process.PdfPlot([process.StockPlotter([process.plot.Graph(title="Stock with bands")],
                                              stock_bands),
                         process.StockPlotter([process.plot.Graph(title="Stock with averages")],
                                              stock_avgs),
                         process.StockPlotter([process.plot.Graph(title="MACD")],
                                              stock_macd),
                         process.StockPlotter([process.plot.Graph(title="RSI")],
                                              stock_rsi),
                         process.StockPlotter([process.plot.Graph(title="Daily returns",
                                                                  ylabel="Return")],
                                              short_tdr),
                         process.StockPlotter([process.plot.Histogram()],
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
    parser.add_argument('-w', '--window', default=30, type=int,
                        help='Calculation window')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    args = parser.parse_args()

    plot_tickers(
        args.tickers,
        args.baseline,
        args.window,
        args.start,
        args.end)


if __name__ == "__main__":
    run()
