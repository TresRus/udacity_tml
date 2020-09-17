import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (FillMissing)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG", "GLD"], ColumnName.ADJCLOSE)

    def test_fill(self):
        self.assertEqual(self.df.isnull().sum().sum(), 60)
        filled_df = FillMissing().process(self.df)
        self.assertEqual(filled_df.isnull().sum().sum(), 0)


if __name__ == '__main__':
    unittest.main()
