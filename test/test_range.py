import unittest
import os
import datetime
import pandas as pd
from trade.data import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (Range)


class TestMerger(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.stock = CsvReader(data_dir).read_stock(
            ["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])

    def test_get_valid_range(self):
        start = "2020-07-01"
        end = "2020-09-01"
        dates = pd.date_range(start, end)
        stock_range = Range(dates).process(self.stock)
        self.assertEqual(
            stock_range.column(
                Column.Name.ADJCLOSE).df.shape[0], 44)
        self.assertEqual(
            stock_range.column(Column.Name.ADJCLOSE).df.index[0],
            datetime.datetime.strptime(
                "2020-07-01",
                "%Y-%m-%d"))

    def test_get_invalid_range(self):
        start = "2020-09-01"
        end = "2020-07-01"
        dates = pd.date_range(start, end)
        stock_range = Range(dates).process(self.stock)
        self.assertEqual(
            stock_range.column(
                Column.Name.ADJCLOSE).df.shape[0], 0)

    def test_get_out_of_range(self):
        start = "2010-07-01"
        end = "2010-09-01"
        dates = pd.date_range(start, end)
        stock_range = Range(dates).process(self.stock)
        self.assertEqual(
            stock_range.column(
                Column.Name.ADJCLOSE).df.shape[0], 0)


if __name__ == '__main__':
    unittest.main()
