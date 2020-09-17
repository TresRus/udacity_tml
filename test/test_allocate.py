import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Allocate)


class TestAllocate(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG"], ColumnName.ADJCLOSE)

    def test_normal(self):
        parts = [0.3, 0.7]
        allocated_df = Allocate(parts).process(self.df)
        self.assertEqual(
            allocated_df.iloc[-1]["SPY"], self.df.iloc[-1]["SPY"] * parts[0])
        self.assertEqual(
            allocated_df.iloc[-1]["GOOG"], self.df.iloc[-1]["GOOG"] * parts[1])

    def test_too_long(self):
        parts = [0.3, 0.3, 0.4]
        with self.assertRaises(ValueError) as context:
            Allocate(parts).process(self.df)

    def test_too_short(self):
        parts = [1.]
        with self.assertRaises(ValueError) as context:
            Allocate(parts).process(self.df)


if __name__ == '__main__':
    unittest.main()
