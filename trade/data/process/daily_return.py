import column_base
from trade.data import Column


class DailyReturn(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.df = (column.df / column.df.shift(1)) - 1
        result_column.df.ix[0, :] = 0
        return result_column
