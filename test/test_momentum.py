import unittest
import os
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Momentum)


class TestMomentum(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(["SPY"], ColumnName.ADJCLOSE)

    def test_normal(self):
        daily_return_df = Momentum(10).process(self.df)
        self.assertEqual(
            daily_return_df.iloc[10]["SPY"],
            self.df.iloc[10]["SPY"] -
            self.df.iloc[0]["SPY"])


if __name__ == '__main__':
    unittest.main()
