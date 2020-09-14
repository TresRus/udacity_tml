import os
import argparse
from pandas_datareader import data as pdr
import yfinance as yf


def load_ticker(ticker, dataDir):
    csv = os.path.join(dataDir, "%s.csv" % ticker)
    print("Download {} to {}".format(ticker, csv))
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker, period="max")
    if not data.empty:
        data.to_csv(csv)


def load_tickers(tickers):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(root_dir, "data")

    for ticker in tickers:
        load_ticker(ticker, data_dir)


def run():
    parser = argparse.ArgumentParser(
        description='Download historic data from yahoo finance.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to download')
    args = parser.parse_args()

    load_tickers(args.tickers)


if __name__ == "__main__":
    run()
