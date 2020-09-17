class Allocate(object):
    def __init__(self, parts):
        self.parts = parts

    def process(self, df):
        if len(self.parts) != len(df.columns):
            raise ValueError("Parts size is not equal to columns size: {} != {}".format(
                len(self.parts), len(df.columns)))

        return df * self.parts
