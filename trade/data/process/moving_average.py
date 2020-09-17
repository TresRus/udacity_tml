class MovingAverage(object):
    def __init__(self, window):
        self.window = int(window)

    def process(self, df):
        result_df = df.rolling(self.window).mean()
        result_df.iloc[0:self.window, :] = df.iloc[0:self.window, :]
        return result_df
