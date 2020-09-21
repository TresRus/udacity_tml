import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Normalize)


class TestNormalize(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY"], ColumnName.ADJCLOSE)

    def test_normalize(self):
        normalized_df = Normalize().process(self.df)
        self.assertEqual(
            normalized_df.max().tolist(),
            (self.df.max() / self.df.iloc[0]).tolist())


if __name__ == '__main__':
    unittest.main()
