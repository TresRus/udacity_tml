from . import column_base
from trade.data import Column


class Tail(column_base.ColumnBase):
    def __init__(self, length):
        self.length = length

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data[-self.length:]
        return result_column
