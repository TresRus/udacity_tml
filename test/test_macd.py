import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Macd)


class TestMacd(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        emad, macd = Macd(10).process(self.df)
        self.assertEqual(emad.shape, self.df.shape)
        self.assertEqual(macd.shape, self.df.shape)


if __name__ == '__main__':
    unittest.main()
