import pandas as pd


class Pipe(object):
    def __init__(self, *args):
        self.processors = args

    def process(self, df):
        result_df = df
        for processor in self.processors:
            result_df = processor.process(result_df)
        return result_df


class Pass(object):
    def process(self, df):
        return df


class Lambda(object):
    def __init__(self, function):
        self.function = function

    def process(self, df):
        return self.function(df)


class Parallel(object):
    def __init__(self, *args):
        self.processors = args

    def process(self, *dfs):
        if len(self.processors) != len(dfs):
            raise ValueError("Number of processors is not equal to number of dataframes size: {} != {}".format(
                len(self.processors), len(dfs)))

        return tuple([processor.process(df)
                      for df, processor in zip(dfs, self.processors)])


class Split(object):
    def __init__(self, *args):
        self.processors = args

    def process(self, df):
        return Parallel(*self.processors).process(*
                                                  ([df] * len(self.processors)))


class Merge(object):
    def process(self, *args):
        result_df = pd.DataFrame()
        for df in args:
            result_df = result_df.join(df, how="outer")
        return result_df
