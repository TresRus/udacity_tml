import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (TickerSuffix)


class TestTickerSuffix(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        suffix_df = TickerSuffix("_test").process(self.df)
        self.assertEqual(suffix_df.columns, ["SPY_test"])


if __name__ == '__main__':
    unittest.main()
