import column_base
from trade.data import storage


class Normalize(column_base.ColumnBase):
    def process_column(self, column):
        result_column = storage.Column(column.name)
        result_column.df = column.df / column.df.ix[0]
        return result_column
