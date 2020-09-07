import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import utils


def optimize(tickers, baseline, start, end):
    if baseline not in tickers:
        tickers += [baseline]

    reader = utils.data.CsvReader()
    stock = reader.read_stock(tickers, [utils.data.Column.Name.ADJCLOSE])
    stock.set_baseline(baseline)
    stock.fill_missing_values()
    
    dates = pd.date_range(start, end)
    stock_range = stock.get_date_range(dates)

    ac_data = stock_range.column(utils.data.Column.Name.ADJCLOSE)
    norm = ac_data.normalize()
    utils.print_statistic(norm, utils.daily_free_risk())

    market = norm[['SPY']]

    result_allocates = ac_data.fit_line(utils.reverse_sr)
    utils.print_allocations(result_allocates, ac_data.df.columns)

    portfolio = ac_data.portfolio_val(result_allocates)
    market = market.join(portfolio)

    utils.print_statistic(market, utils.daily_free_risk())

    utils.plot_data(market)


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

    optimize(args.tickers, args.baseline, args.start, args.end)


if __name__ == "__main__":
    run()
