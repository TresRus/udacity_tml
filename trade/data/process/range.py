import pandas as pd
import column_base
from trade.data import storage

class Range(column_base.ColumnBase):
    def __init__(self, dates):
        self.dates = dates

    def process_column(self, column):
        result_column = storage.Column(column.name)
        result_column.df = pd.DataFrame(index=self.dates)
        result_column.df = result_column.df.join(column.df, how="inner")
        return result_column
