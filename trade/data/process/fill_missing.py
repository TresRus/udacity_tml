class FillMissing(object):
    def process(self, df):
        result_df = df.fillna(method='ffill')
        result_df.fillna(method='bfill', inplace=True)
        return result_df
