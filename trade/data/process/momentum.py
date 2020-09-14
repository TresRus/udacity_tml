from . import column_base
from trade.data import Column


class Momentum(column_base.ColumnBase):
    def __init__(self, window):
        self.window = window

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = (column.data - column.data.shift(self.window))
        result_column.data.ix[0:self.window, :] = 0
        return result_column
