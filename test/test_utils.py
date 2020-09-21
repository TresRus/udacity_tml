import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Pipe, Pass, Lambda, Parallel, Split, Merge)


class TestPass(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_pass(self):
        passed_df = Pass().process(self.df)
        self.assertTrue(passed_df.equals(self.df))


class TestLambda(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_lambda(self):
        result_df = Lambda(lambda x: x + 1).process(self.df)
        self.assertTrue(result_df.iloc[0]["SPY"], self.df.iloc[0]["SPY"] + 1)


class TestPipe(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_pipe_lambda(self):
        result_df = Pipe(
            Lambda(lambda x: x + 1),
            Lambda(lambda x: x * 2)
        ).process(self.df)
        self.assertTrue(
            result_df.iloc[0]["SPY"],
            (self.df.iloc[0]["SPY"] + 1) * 2)


class TestParallel(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.dfs = [
            CsvReader(data_dir).read_column(
                ["SPY"], ColumnName.ADJCLOSE), CsvReader(data_dir).read_column(
                ["GOOG"], ColumnName.ADJCLOSE)]

    def test_pass_lambda(self):
        result = Parallel(
            Pass(),
            Lambda(lambda x: x * 2)
        ).process(self.dfs)
        self.assertTrue(result[0].iloc[0]["SPY"], self.dfs[0].iloc[0]["SPY"])
        self.assertTrue(
            result[1].iloc[0]["GOOG"],
            self.dfs[1].iloc[0]["GOOG"] * 2)


class TestSplit(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_pass_lambda(self):
        result = Split(
            Pass(),
            Lambda(lambda x: x * 2)
        ).process(self.df)
        self.assertTrue(result[0].iloc[0]["SPY"], self.df.iloc[0]["SPY"])
        self.assertTrue(result[1].iloc[0]["SPY"], self.df.iloc[0]["SPY"] * 2)


class TestMerge(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_merge_tickers(self):
        df_a = self.reader.read_column(["GOOG"], ColumnName.ADJCLOSE)
        df_b = self.reader.read_column(["GLD"], ColumnName.ADJCLOSE)
        df_c = Merge().process(df_a, df_b)
        self.assertListEqual(df_c.columns.tolist(), ["GOOG", "GLD"])


if __name__ == '__main__':
    unittest.main()
