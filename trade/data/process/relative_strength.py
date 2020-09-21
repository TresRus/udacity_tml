class RelativeStrength(object):
    def __init__(self, window):
        self.window = window

    def process(self, df):
        delta = df.diff()

        up = delta.copy()
        up[up < 0] = 0
        up = up.ewm(span=self.window).mean().abs()

        down = delta.copy()
        down[down > 0] = 0
        down = down.ewm(span=self.window).mean().abs()

        result_df = up / down
        result_df.fillna(method='ffill', inplace=True)
        return result_df


class RelativeStrengthIndex(object):
    def __init__(self, window):
        self.window = window

    def process(self, df):
        return 100 - 100 / (1 + RelativeStrength(self.window).process(df))
