from . import column_base
from trade.data import Column


class Sum(column_base.ColumnBase):
    def __init__(self, name):
        self.name = name

    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data.sum(axis=1)
        result_column.data.name = "Portfolio"
        result_column.data = result_column.data.to_frame()
        return result_column
