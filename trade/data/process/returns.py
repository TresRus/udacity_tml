class DailyReturn(object):
    def process(self, df):
        result_df = (df / df.shift(1)) - 1.
        result_df.iloc[0, :] = 0.
        return result_df

class CumulativeReturn(object):
    def process(self, df):
        return (df / df.iloc[0]) - 1.

class ReverseCumulativeReturn(object):
    def process(self, df):
        return (1. + df)
