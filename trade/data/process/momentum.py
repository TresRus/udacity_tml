class Momentum(object):
    def __init__(self, window):
        self.window = window

    def process(self, df):
        result_df = (df - df.shift(self.window))
        result_df.iloc[0:self.window, :] = 0
        return result_df
