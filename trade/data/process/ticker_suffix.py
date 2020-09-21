class TickerSuffix(object):
    def __init__(self, suffix):
        self.suffix = suffix

    def process(self, df):
        renames = {}
        for name in df.columns:
            renames[name] = "{}{}".format(name, self.suffix)
        return df.rename(columns=renames)
