import os
import argparse
import pandas as pd
from trade.data import (ColumnName, reader, process)
from trade.data.process import (plot)
import trade.type


def plot_tickers(tickers, baseline, window, start, end):
    dates = pd.date_range(start, end)

    data, norm_data, daily_return = process.Pipe(
        process.FillMissing(),
        process.Range(dates),
        process.Split(
            process.Pass(),
            process.Normalize(),
            process.DailyReturn()
        )
    ).process(reader.CsvReader().read_column(tickers + [baseline], ColumnName.ADJCLOSE))

    root_dir = os.path.dirname(os.path.realpath(__file__))
    plot_dir = os.path.join(root_dir, "plots")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plot_path = os.path.join(plot_dir, "Market.pdf")
    plot.PdfPlot(plot_path,
        plot.DfPlotter(norm_data, plot.Graph()),
        plot.DfPlotter(daily_return, plot.Histogram(baseline=baseline))
    ).plot()

    for ticker in tickers:
        plot_path = os.path.join(plot_dir, "{}.pdf".format(ticker))


        t_data, t_daily_return, tb_daily_return = process.Parallel(
            process.Filter([ticker]),
            process.Filter([ticker]),
            process.Filter([ticker, baseline])
        ).process([data, daily_return, daily_return])

        bands = process.Pipe(
            process.Split(
                process.Pass(),
                process.Pipe(
                    process.TickerSuffix("_mov_avg({})".format(window)),
                    process.MovingAverage(window)
                ),
                process.Pipe(
                    process.BollingerBands(window),
                    process.Parallel(
                        process.TickerSuffix("_upper_bb({})".format(window)),
                        process.TickerSuffix("_lower_bb({})".format(window))
                    ),
                    process.Merge()
                )
            ),
            process.Merge(),
            process.Tail(window * 3)
        ).process(t_data)

        avgs = process.Pipe(
            process.Split(
                process.Pass(),
                process.Pipe(
                    process.TickerSuffix("_mov_avg({})".format(window / 2)),
                    process.MovingAverage(window / 2)
                ),
                process.Pipe(
                    process.TickerSuffix("_mov_avg({})".format(window / 4)),
                    process.MovingAverage(window / 4)
                )
            ),
            process.Merge(),
            process.Tail(window * 3)
        ).process(t_data)

        macd = process.Pipe(
            process.Macd(window),
            process.Parallel(
                process.TickerSuffix("_emad({})".format(window)),
                process.TickerSuffix("_macd({})".format(window))
            ),
            process.Merge(),
            process.Tail(window * 3)
        ).process(t_data)

        rsi = process.Pipe(
            process.RelativeStrengthIndex(window),
            process.TickerSuffix("_rsi({})".format(window)),
            process.Merge(),
            process.Tail(window * 3)
        ).process(t_data)

        st_daily_return = process.Tail(window * 3).process(t_daily_return)

        plot.PdfPlot(plot_path,
            plot.DfPlotter(bands, plot.Graph(title="Stock with bands")),
            plot.DfPlotter(avgs, plot.Graph(title="Stock with averages")),
            plot.DfPlotter(macd, plot.Graph(title="MACD")),
            plot.DfPlotter(rsi, plot.Graph(title="RSI")),
            plot.DfPlotter(st_daily_return, plot.Graph(title="Daily return", ylabel="Return")),
            plot.DfPlotter(t_daily_return, plot.Histogram()),
            plot.DfPlotter(tb_daily_return, plot.Scatter(baseline))
        ).plot()


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
