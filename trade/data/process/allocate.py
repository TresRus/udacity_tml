import column_base
from trade.data import Column


class Allocate(column_base.ColumnBase):
    def __init__(self, parts):
        self.parts = parts

    def process_column(self, column):
        if len(self.parts) != len(column.data.columns):
            raise ValueError(
                "Column {}: Parts size is not equal to columns size: {} != {}".format(
                    column.name, len(self.parts), len(column.data.columns)))

        result_column = Column(column.name)
        result_column.data = column.data * self.parts
        return result_column
