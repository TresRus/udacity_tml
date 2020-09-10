import unittest
import os
from trade.data import (Column)
from trade.data.reader import (CsvReader)
from trade.data.process import (Baseline)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.stock = CsvReader(data_dir).read_stock(
            ["SPY", "GOOG", "GLD"], [Column.Name.ADJCLOSE])

    def test_spy(self):
        baseline_stock = Baseline("SPY").process(self.stock)
        self.assertEqual(
            baseline_stock.column(
                Column.Name.ADJCLOSE).df.shape[0], 50)

    def test_goog(self):
        baseline_stock = Baseline("GOOG").process(self.stock)
        self.assertEqual(
            baseline_stock.column(
                Column.Name.ADJCLOSE).df.shape[0], 30)

    def test_xom(self):
        with self.assertRaises(ValueError) as context:
            baseline_stock = Baseline("XOM").process(self.stock)


if __name__ == '__main__':
    unittest.main()
