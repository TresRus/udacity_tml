from trade.data import storage

class Merger(object):
    def process(self, stock_a, stock_b):
        result_stock = storage.Stock()

        for name, column in stock_a.data.iteritems():
            result_column = result_stock.column(name)
            result_column.df = result_column.df.join(column.df, how="outer")

        for name, column in stock_b.data.iteritems():
            result_column = result_stock.column(name)
            result_column.df = result_column.df.join(column.df, how="outer")

        return result_stock

