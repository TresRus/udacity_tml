import unittest
import os
from trade.data.storage import (Stock, Column)
from trade.data.reader import (CsvReader)


class TestMarket(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_read_spy(self):
        stock = self.reader.read_stock(["SPY"], [Column.Name.ADJCLOSE])
        self.assertEqual(stock.column(Column.Name.ADJCLOSE).df.shape[0], 50)

    def test_read_goog(self):
        stock = self.reader.read_stock(["GOOG"], [Column.Name.ADJCLOSE])
        self.assertEqual(stock.column(Column.Name.ADJCLOSE).df.shape[0], 30)

    def test_read_gld(self):
        stock = self.reader.read_stock(["GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(stock.column(Column.Name.ADJCLOSE).df.shape[0], 70)

    def test_read_all(self):
        stock = self.reader.read_stock(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(stock.column(Column.Name.ADJCLOSE).df.shape[0], 70)

    def test_fill(self):
        stock = self.reader.read_stock(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(
            stock.column(Column.Name.ADJCLOSE).df.isnull().sum().sum(), 60)
        stock.fill_missing_values()
        self.assertEqual(
            stock.column(Column.Name.ADJCLOSE).df.isnull().sum().sum(), 0)


class TestColumn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_read_spy(self):
        column = self.reader.read_column(["SPY"], Column.Name.ADJCLOSE)
        self.assertEqual(column.df.shape[0], 50)

    def test_read_goog(self):
        column = self.reader.read_column(["GOOG"], Column.Name.ADJCLOSE)
        self.assertEqual(column.df.shape[0], 30)

    def test_read_gld(self):
        column = self.reader.read_column(["GLD"], Column.Name.ADJCLOSE)
        self.assertEqual(column.df.shape[0], 70)

    def test_read_all(self):
        column = self.reader.read_column(["SPY", "GOOG", "GLD"], Column.Name.ADJCLOSE)
        self.assertEqual(column.df.shape[0], 70)

    def test_fill(self):
        column = self.reader.read_column(["SPY", "GOOG", "GLD"], Column.Name.ADJCLOSE)
        self.assertEqual(column.df.isnull().sum().sum(), 60)
        column.fill_missing_values()
        self.assertEqual(column.df.isnull().sum().sum(), 0)

if __name__ == '__main__':
    unittest.main()
