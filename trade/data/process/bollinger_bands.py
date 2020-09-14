import column_base
from trade.data import Column
from moving_average import MovingAverage
from moving_std import MovingStd


class UpperBollingerBand(column_base.ColumnBase):
    def __init__(self, window):
        self.ma_p = MovingAverage(window)
        self.ms_p = MovingStd(window)

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = self.ma_p.process_column(column).data + self.ms_p.process_column(column).data * 2
        return result_column


class LowerBollingerBand(column_base.ColumnBase):
    def __init__(self, window):
        self.ma_p = MovingAverage(window)
        self.ms_p = MovingStd(window)

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = self.ma_p.process_column(column).data - self.ms_p.process_column(column).data * 2
        return result_column
