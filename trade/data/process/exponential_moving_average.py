from . import column_base
from trade.data import Column


class ExponentialMovingAverage(column_base.ColumnBase):
    def __init__(self, window):
        self.window = int(window)

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.ewm(span=self.window).mean()
        result_column.data.iloc[0:self.window,
                                :] = column.data.iloc[0:self.window, :]
        return result_column
