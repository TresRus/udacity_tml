from . import column_base
from .exponential_moving_average import ExponentialMovingAverage
from trade.data import Column


class Emad(column_base.ColumnBase):
    def __init__(self, window):
        self.emal_p = ExponentialMovingAverage(window)
        self.emas_p = ExponentialMovingAverage(window / 2)

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = self.emas_p.process_column(
            column).data - self.emal_p.process_column(column).data
        return result_column
