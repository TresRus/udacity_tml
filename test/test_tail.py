import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Tail)


class TestMerger(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG", "GLD"], ColumnName.ADJCLOSE)

    def test_normal(self):
        tail_df = Tail(30).process(self.df)
        self.assertEqual(tail_df.shape[0], 30)


if __name__ == '__main__':
    unittest.main()
