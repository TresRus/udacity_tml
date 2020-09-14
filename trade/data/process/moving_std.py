from . import column_base
from trade.data import Column


class MovingStd(column_base.ColumnBase):
    def __init__(self, window):
        self.window = window

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.rolling(self.window).std()
        result_column.data.iloc[0:self.window, :] = 0
        return result_column
