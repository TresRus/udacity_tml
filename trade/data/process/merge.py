from trade.data import Stock


class Merger(object):
    def process(self, stocks):
        result_stock = Stock()

        for stock in stocks:
            for name, column in stock.columns.iteritems():
                result_column = result_stock.column(name)
                result_column.data = result_column.data.join(
                    column.data, how="outer")

        return result_stock
