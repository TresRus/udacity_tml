import column_base
from trade.data import Column


class Filter(column_base.ColumnBase):
    def __init__(self, tickers):
        self.tickers = tickers

    def process_column(self, column):
        for ticker in self.tickers:
            if ticker not in column.data.columns:
                raise ValueError(
                    "No {} ticker in {} column".format(
                        ticker, column.name))

        result_column = Column(column.name)
        result_column.data = column.data[self.tickers]
        return result_column
