import column_base
from trade.data import Column


class Baseline(column_base.ColumnBase):
    def __init__(self, ticker):
        self.ticker = ticker

    def process_column(self, column):
        if self.ticker not in column.df.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.ticker, column.name))

        result_column = Column(column.name)
        result_column.df = column.df.dropna(subset=[self.ticker])
        return result_column
