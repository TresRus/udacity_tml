import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (MovingAverage)


class TestMovingAvg(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        ma_df = MovingAverage(10).process(self.df)
        self.assertEqual(ma_df.shape, self.df.shape)


if __name__ == '__main__':
    unittest.main()
