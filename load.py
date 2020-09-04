import os
import argparse
from pandas_datareader import data as pdr
import yfinance as yf

def loadTicker(ticker, dataDir):
    csv = os.path.join(dataDir, "%s.csv" % ticker)
    print "Download %s to %s" % (ticker, csv)
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    yf.pdr_override()
    data = pdr.get_data_yahoo(ticker, period="max")
    if not data.empty:
        data.to_csv(csv)

def run():
    parser = argparse.ArgumentParser(description='Download historic data from yahoo finance.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to download')
    args = parser.parse_args()

    rootDir = os.path.dirname(os.path.realpath(__file__))
    dataDir = os.path.join( rootDir, "data" )

    for ticker in args.tickers:
        loadTicker( ticker, dataDir )

if __name__ == "__main__":
    run()
