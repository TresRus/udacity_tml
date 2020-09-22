import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Normalize, DailyReturn, CumulativeReturn, ReverseCumulativeReturn)


class TestDailyReturn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        daily_return_df = DailyReturn().process(self.df)
        self.assertEqual(
            daily_return_df.iloc[1]["SPY"],
            self.df.iloc[1]["SPY"] /
            self.df.iloc[0]["SPY"] -
            1.)

class TestCumulativeReturn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        cr_df = CumulativeReturn().process(self.df)
        self.assertEqual(
            cr_df.iloc[-1]["SPY"],
            self.df.iloc[-1]["SPY"] /
            self.df.iloc[0]["SPY"] -
            1.)

class TestReverseCumulativeReturn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        ndf = Normalize().process(self.df)
        cr_df = CumulativeReturn().process(self.df)
        rcr_df = ReverseCumulativeReturn().process(cr_df)
        self.assertTrue(ndf.equals(rcr_df))

if __name__ == '__main__':
    unittest.main()
