from trade.data import storage


class Merger(object):
    def process(self, stocks):
        result_stock = storage.Stock()

        for stock in stocks:
            for name, column in stock.columns.iteritems():
                result_column = result_stock.column(name)
                result_column.df = result_column.df.join(
                    column.df, how="outer")

        return result_stock
