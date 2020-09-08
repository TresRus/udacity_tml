import pandas as pd
from trade.data import storage

class Range(object):
    def __init__(self, dates):
        self.dates = dates

    def _process_column(self, column):
        result_column = storage.Column(column.name)
        result_column.df = pd.DataFrame(index=self.dates)
        result_column.df = result_column.df.join(column.df, how="inner")
        return result_column

    def process(self, stock):
        result_stock = storage.Stock()

        for name, column in stock.data.iteritems():
            result_stock.data[name] = self._process_column(column)

        return result_stock
