from . import column_base
from trade.data import Column


class Normalize(column_base.ColumnBase):
    def process_column(self, column):
        result_column = Column(column.name)
        result_column.data = column.data / column.data.iloc[0]
        return result_column
