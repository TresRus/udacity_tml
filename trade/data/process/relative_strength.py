from . import column_base
from trade.data import Column


class RelativeStrength(column_base.ColumnBase):
    def __init__(self, window):
        self.window = window

    def process_column(self, column):
        delta = column.data.diff()

        up = delta.copy()
        up[up < 0] = 0
        up = up.ewm(span=self.window).mean().abs()

        down = delta.copy()
        down[down > 0] = 0
        down = down.ewm(span=self.window).mean().abs()

        result_column = Column(column.name)
        result_column.data = up / down
        result_column.data.fillna(method='ffill', inplace=True)
        return result_column


class RelativeStrengthIndex(column_base.ColumnBase):
    def __init__(self, window):
        self.rs_p = RelativeStrength(window)

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = 100 - 100 / \
            (1 + self.rs_p.process_column(column).data)
        return result_column
