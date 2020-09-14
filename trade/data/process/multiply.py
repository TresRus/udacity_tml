from . import column_base
from trade.data import Column


class Multiply(column_base.ColumnBase):
    def __init__(self, number):
        self.number = number

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data * self.number
        return result_column
