from trade.data.column import Column
import trade.data.column


class Stock(object):
    def __init__(self):
        self.columns = {}

    def __str__(self):
        text = []
        for name, column in self.columns.iteritems():
            text.append("Column {}:".format(name))
            text.append(str(column))
        return "\n".join(text)

    def column(self, name):
        if name not in self.columns:
            self.columns[name] = Column(name)

        return self.columns[name]
