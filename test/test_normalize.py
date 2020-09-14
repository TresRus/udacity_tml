import unittest
import os
from trade.data import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (Normalize)


class TestNormalize(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.stock = CsvReader(data_dir).read_stock(
            ["SPY"], [Column.Name.ADJCLOSE])

    def test_normalize(self):
        normalize_stock = Normalize().process(self.stock)
        self.assertEqual(
            normalize_stock.column(
                Column.Name.ADJCLOSE).data.max().tolist(),
            (self.stock.column(
                Column.Name.ADJCLOSE).data.max() /
             self.stock.column(
                Column.Name.ADJCLOSE).data.iloc[0]).tolist())


if __name__ == '__main__':
    unittest.main()
