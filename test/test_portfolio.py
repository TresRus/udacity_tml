import unittest
import os
from trade.type import (Allocation, AllocationSet)
from trade.data import (ColumnName)
from trade.data.reader import (CsvReader)
from trade.data.process import (Portfolio, PortfolioSet)


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG"], ColumnName.ADJCLOSE)

    def test_normal(self):
        allocations = [Allocation("SPY", 30), Allocation("GOOG", 70)]
        portfolio = Portfolio(allocations).process(self.df)
        self.assertEqual(portfolio.shape[0], self.df.shape[0])
        self.assertEqual(portfolio.shape[1], 1)

    def test_order(self):
        allocations_a = [Allocation("SPY", 30), Allocation("GOOG", 70)]
        portfolio_a = Portfolio(allocations_a).process(self.df)
        allocations_b = [Allocation("GOOG", 70), Allocation("SPY", 30)]
        portfolio_b = Portfolio(allocations_b).process(self.df)
        self.assertTrue(portfolio_a.equals(portfolio_b))

    def test_partial(self):
        allocations = [Allocation("SPY", 30)]
        portfolio = Portfolio(allocations).process(self.df)
        self.assertEqual(portfolio.shape[0], self.df.shape[0])
        self.assertEqual(portfolio.shape[1], 1)

    def test_wrong_ticker(self):
        allocations = [Allocation("GLD", 30), Allocation("GOOG", 70)]
        with self.assertRaises(ValueError) as context:
            Portfolio(allocations).process(self.df)

    def test_too_long(self):
        allocations = [
            Allocation(
                "SPY", 30), Allocation(
                "GOOG", 40), Allocation(
                "GLD", 30)]
        with self.assertRaises(ValueError) as context:
            Portfolio(allocations).process(self.df)

class TestPortfolioSet(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(root_dir, "data")
        self.df = CsvReader(data_dir).read_column(
            ["SPY", "GOOG"], ColumnName.ADJCLOSE)

    def test_normal(self):
        allocations = [Allocation("SPY", 30), Allocation("GOOG", 70)]
        portfolio_set = PortfolioSet(allocations, 20000).process(self.df)
        self.assertEqual(portfolio_set.data["SPY"], 17)
        self.assertEqual(portfolio_set.data["GOOG"], 8)


if __name__ == '__main__':
    unittest.main()
