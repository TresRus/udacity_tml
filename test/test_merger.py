import unittest
import os
from trade.data.storage import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (Merger)


class TestMerger(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_merge_different_tickers(self):
        stock_a = self.reader.read_stock(["GOOG"], [Column.Name.ADJCLOSE])
        stock_b = self.reader.read_stock(["GLD"], [Column.Name.ADJCLOSE])
        stock_c = Merger().process([stock_a, stock_b])
        self.assertEqual(len(stock_c.columns), 1)
        self.assertEqual(stock_c.column(Column.Name.ADJCLOSE).df.shape[1], 2)

    def test_merge_different_columns(self):
        stock_a = self.reader.read_stock(["GOOG"], [Column.Name.ADJCLOSE])
        stock_b = self.reader.read_stock(["GLD"], [Column.Name.CLOSE])
        stock_c = Merger().process([stock_a, stock_b])
        self.assertEqual(len(stock_c.columns), 2)
        self.assertEqual(stock_c.column(Column.Name.ADJCLOSE).df.shape[1], 1)
        self.assertEqual(stock_c.column(Column.Name.CLOSE).df.shape[1], 1)


if __name__ == '__main__':
    unittest.main()
