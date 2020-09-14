import pandas as pd
from . import column_base
from trade.data import Column


class Range(column_base.ColumnBase):
    def __init__(self, dates):
        self.dates = dates

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = pd.DataFrame(index=self.dates)
        result_column.data = result_column.data.join(column.data, how="inner")
        return result_column
