from trade.data import storage


class ColumnBase(object):
    def process_column(self, column):
        raise NotImplementedError

    def process(self, stock):
        result_stock = storage.Stock()

        for name, column in stock.columns.iteritems():
            result_stock.columns[name] = self.process_column(column)

        return result_stock
