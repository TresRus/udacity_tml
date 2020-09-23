class Normalize(object):
    def process(self, df):
        return df / df.iloc[0]

class NormalizeIndicator(object):
    def process(self, df):
        return (df - df.mean()) / df.std()
