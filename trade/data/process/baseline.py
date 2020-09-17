class Baseline(object):
    def __init__(self, ticker):
        self.ticker = ticker

    def process(self, df):
        if self.ticker not in df.columns:
            raise ValueError("No {} ticker in dataframe".format(self.ticker))

        return df.dropna(subset=[self.ticker])
