import os
import argparse
import datetime
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf


def create_usd(csv):
    now = datetime.datetime.now()
    dates = pd.date_range(
        datetime.date(now.year - 40, now.month, now.day),
        datetime.date(now.year, now.month, now.day))
    df = pd.DataFrame(
        1.0,
        index=pd.Index(data=dates, name="Date"),
        columns=["Open", "High", "Low", "Close", "Adj Close", "Volume"])
    df.to_csv(csv)

def load_ticker(ticker, dataDir):
    csv = os.path.join(dataDir, "%s.csv" % ticker)
    print("Download {} to {}".format(ticker, csv))
    if ticker == "usd":
        create_usd(csv)
        return
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
