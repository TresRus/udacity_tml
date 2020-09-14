import column_base
from trade.data import Column


class MovingAverage(column_base.ColumnBase):
    def __init__(self, window):
        self.window = window

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.rolling(self.window).mean()
        result_column.data.ix[0:self.window,
                              :] = column.data.ix[0:self.window, :]
        return result_column
