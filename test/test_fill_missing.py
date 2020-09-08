import unittest
import os
from trade.data.storage import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (FillMissing)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.stock = CsvReader(data_dir).read_stock(
            ["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])

    def test_fill(self):
        self.assertEqual(
            self.stock.column(
                Column.Name.ADJCLOSE).df.isnull().sum().sum(),
            60)
        filled_stock = FillMissing().process(self.stock)
        self.assertEqual(
            filled_stock.column(
                Column.Name.ADJCLOSE).df.isnull().sum().sum(), 0)


if __name__ == '__main__':
    unittest.main()
