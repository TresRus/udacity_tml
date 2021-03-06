import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (BollingerBands, BB)


class TestBollingerBands(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        ubb_df, lbb_df = BollingerBands(10).process(self.df)
        self.assertLess(lbb_df.iloc[-1]["SPY"], ubb_df.iloc[-1]["SPY"])

    def test_indicator(self):
        bb = BB(10).process(self.df)
        self.assertEqual(bb.shape, self.df.shape)


if __name__ == '__main__':
    unittest.main()
