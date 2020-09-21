import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Sum)


class TestSum(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG"], ColumnName.ADJCLOSE)

    def test_normal(self):
        sum_df = Sum("Sum").process(self.df)
        self.assertEqual(sum_df.shape[0], self.df.shape[0])
        self.assertEqual(sum_df.shape[1], 1)
        self.assertEqual(
            sum_df.iloc[-1]["Sum"], self.df.iloc[-1]["SPY"] + self.df.iloc[-1]["GOOG"])
