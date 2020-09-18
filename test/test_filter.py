import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Filter)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG", "GLD"], ColumnName.ADJCLOSE)

    def test_spy(self):
        filtered_df = Filter(["SPY"]).process(self.df)
        self.assertListEqual(filtered_df.columns.tolist(), ["SPY"])

    def test_goog(self):
        filtered_df = Filter(["GOOG"]).process(self.df)
        self.assertListEqual(filtered_df.columns.tolist(), ["GOOG"])

    def test_two(self):
        filtered_df = Filter(["SPY", "GOOG"]).process(self.df)
        self.assertListEqual(filtered_df.columns.tolist(), ["SPY", "GOOG"])

    def test_xom(self):
        with self.assertRaises(ValueError) as context:
            Filter(["XOM"]).process(self.df)


if __name__ == '__main__':
    unittest.main()
