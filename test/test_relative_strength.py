import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (RelativeStrength, RelativeStrengthIndex)


class TestRelativeStrength(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        rs_df = RelativeStrength(10).process(self.df)
        self.assertEqual(rs_df.shape, self.df.shape)


class TestRelativeStrengthIndex(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        rsi_df = RelativeStrengthIndex(10).process(self.df)
        self.assertEqual(rsi_df.shape, self.df.shape)


if __name__ == '__main__':
    unittest.main()
