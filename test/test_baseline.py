import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Baseline)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG", "GLD"], ColumnName.ADJCLOSE)

    def test_spy(self):
        baseline_df = Baseline("SPY").process(self.df)
        self.assertEqual(baseline_df.shape[0], 50)

    def test_goog(self):
        baseline_df = Baseline("GOOG").process(self.df)
        self.assertEqual(baseline_df.shape[0], 30)

    def test_xom(self):
        with self.assertRaises(ValueError) as context:
            Baseline("XOM").process(self.df)


if __name__ == '__main__':
    unittest.main()
