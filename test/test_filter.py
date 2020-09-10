import unittest
import os
from trade.data import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (Filter)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.stock = CsvReader(data_dir).read_stock(
            ["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])

    def test_spy(self):
        filtered_stock = Filter(["SPY"]).process(self.stock)
        self.assertListEqual(
            filtered_stock.column(
                Column.Name.ADJCLOSE).df.columns.tolist(), ["SPY"])

    def test_goog(self):
        filtered_stock = Filter(["GOOG"]).process(self.stock)
        self.assertListEqual(
            filtered_stock.column(
                Column.Name.ADJCLOSE).df.columns.tolist(), ["GOOG"])

    def test_two(self):
        filtered_stock = Filter(["SPY", "GOOG"]).process(self.stock)
        self.assertListEqual(
            filtered_stock.column(
                Column.Name.ADJCLOSE).df.columns.tolist(), ["SPY", "GOOG"])

    def test_xom(self):
        with self.assertRaises(ValueError) as context:
            filtered_stock = Filter("XOM").process(self.stock)


if __name__ == '__main__':
    unittest.main()
