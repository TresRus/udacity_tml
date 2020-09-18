class Filter(object):
    def __init__(self, tickers):
        self.tickers = tickers

    def process(self, df):
        for ticker in self.tickers:
            if ticker not in df.columns:
                raise ValueError("No {} ticker in dataframe".format(ticker))

        return df[self.tickers]
