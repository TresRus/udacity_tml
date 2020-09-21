import pandas as pd


class Range(object):
    def __init__(self, dates):
        self.dates = dates

    def process(self, df):
        result_df = pd.DataFrame(index=self.dates)
        result_df = result_df.join(df, how="inner")
        return result_df
