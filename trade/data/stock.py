from trade.data.column import Column
import trade.data.column

class Statistic(object):
    def __init__(self, stock):
        self.columns = {}
        for name, column in stock.columns.iteritems():
            self.columns[name] = trade.data.column.Statistic(column)


class Stock(object):
    def __init__(self):
        self.columns = {}

    def column(self, name):
        if name not in self.columns:
            self.columns[name] = Column(name)

        return self.columns[name]
