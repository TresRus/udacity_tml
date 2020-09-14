import column_base
from trade.data import Column


class TickerSuffix(column_base.ColumnBase):
    def __init__(self, suffix):
        self.suffix = suffix

    def process_column(self, column):
        renames = {}
        for name in column.data.columns:
            renames[name] = "{}{}".format(name, self.suffix)
        result_column = Column(column.name)
        result_column.data = column.data.rename(columns=renames)
        return result_column
