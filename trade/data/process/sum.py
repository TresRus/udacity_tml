class Sum(object):
    def __init__(self, name):
        self.name = name

    def process(self, df):
        result_df = df.sum(axis=1)
        result_df.name = self.name
        result_df = result_df.to_frame()
        return result_df
