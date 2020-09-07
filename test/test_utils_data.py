import unittest
import os
import datetime
import pandas as pd
from trade.utils.data import (Market, CsvReader, Column)


class TestMarket(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.join(root_dir, "data")

    def test_read_spy(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["SPY"], [Column.Name.ADJCLOSE])
        self.assertEqual(m.data[Column.Name.ADJCLOSE].df.shape[0], 50)

    def test_read_goog(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["GOOG"], [Column.Name.ADJCLOSE])
        self.assertEqual(m.data[Column.Name.ADJCLOSE].df.shape[0], 30)

    def test_read_gld(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(m.data[Column.Name.ADJCLOSE].df.shape[0], 70)

    def test_read_all(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(m.data[Column.Name.ADJCLOSE].df.shape[0], 70)

    def test_baseline(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])
        m.set_baseline("SPY")
        self.assertEqual(m.data[Column.Name.ADJCLOSE].df.shape[0], 50)

    def test_fill(self):
        m = Market(CsvReader(self.data_dir))
        m.load(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])
        self.assertEqual(
            m.data[Column.Name.ADJCLOSE].df.isnull().sum().sum(), 60)
        m.fill_missing_values()
        self.assertEqual(
            m.data[Column.Name.ADJCLOSE].df.isnull().sum().sum(), 0)


class TestColumn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.market = Market(CsvReader(data_dir))
        self.market.load(["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])

    def test_baseline(self):
        column = self.market.column(Column.Name.ADJCLOSE)
        column.set_baseline("SPY")
        self.assertEqual(column.df.shape[0], 50)

    def test_fill(self):
        column = self.market.column(Column.Name.ADJCLOSE)
        self.assertEqual(column.df.isnull().sum().sum(), 60)
        column.fill_missing_values()
        self.assertEqual(column.df.isnull().sum().sum(), 0)

    def test_get_date_range(self):
        column = self.market.column(Column.Name.ADJCLOSE)
        start = "2020-07-01"
        end = "2020-09-01"
        dates = pd.date_range(start, end)
        df = column.get_date_range(dates)
        self.assertEqual(df.shape[0], 44)
        self.assertEqual(
            df.index[0],
            datetime.datetime.strptime(
                "2020-07-01",
                "%Y-%m-%d"))


if __name__ == '__main__':
    unittest.main()
