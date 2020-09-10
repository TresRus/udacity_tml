import column_base
from trade.data import Column


class FillMissing(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.df = column.df.fillna(method='ffill')
        result_column.df.fillna(method='bfill', inplace=True)
        return result_column
