class Normalize(object):
    def process(self, df):
        return df / df.iloc[0]
