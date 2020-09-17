class MovingStd(object):
    def __init__(self, window):
        self.window = int(window)

    def process(self, df):
        result_df = df.rolling(self.window).std()
        result_df.iloc[0:self.window, :] = 0
        return result_df
