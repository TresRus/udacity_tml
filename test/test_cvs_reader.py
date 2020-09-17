import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)


class TestDataset(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_read_spy(self):
        dataset = self.reader.read_dataset(["SPY"], [ColumnName.ADJCLOSE])
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[0], 50)
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[1], 1)

    def test_read_goog(self):
        dataset = self.reader.read_dataset(["GOOG"], [ColumnName.ADJCLOSE])
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[0], 30)
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[1], 1)

    def test_read_gld(self):
        dataset = self.reader.read_dataset(["GLD"], [ColumnName.ADJCLOSE])
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[0], 70)
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[1], 1)

    def test_read_all(self):
        dataset = self.reader.read_dataset(
            ["SPY", "GOOG", "GLD"], [ColumnName.ADJCLOSE])
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[0], 70)
        self.assertEqual(dataset.column(ColumnName.ADJCLOSE).shape[1], 3)

    def test_read_multycol(self):
        dataset = self.reader.read_dataset(
            ["SPY"], [ColumnName.CLOSE, ColumnName.ADJCLOSE])
        self.assertEqual(len(dataset.columns), 2)


class TestColumn(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.reader = CsvReader(data_dir)

    def test_read_spy(self):
        df = self.reader.read_column(["SPY"], ColumnName.ADJCLOSE)
        self.assertEqual(df.shape[0], 50)
        self.assertEqual(df.shape[1], 1)

    def test_read_goog(self):
        df = self.reader.read_column(["GOOG"], ColumnName.ADJCLOSE)
        self.assertEqual(df.shape[0], 30)
        self.assertEqual(df.shape[1], 1)

    def test_read_gld(self):
        df = self.reader.read_column(["GLD"], ColumnName.ADJCLOSE)
        self.assertEqual(df.shape[0], 70)
        self.assertEqual(df.shape[1], 1)

    def test_read_all(self):
        df = self.reader.read_column(
            ["SPY", "GOOG", "GLD"], ColumnName.ADJCLOSE)
        self.assertEqual(df.shape[0], 70)
        self.assertEqual(df.shape[1], 3)


if __name__ == '__main__':
    unittest.main()
