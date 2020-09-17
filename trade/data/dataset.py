class ColumnName(object):
    DATE = "Date"
    ADJCLOSE = "Adj Close"
    CLOSE = "Close"
    HIGH = "High"
    LOW = "Low"
    OPEN = "Open"
    VOLUME = "Volume"


class Dataset(object):
    def __init__(self):
        self.columns = {}

    def __str__(self):
        text = []
        for name, column in self.columns.items():
            text.append("Column {}:".format(name))
            text.append(str(column))
        return "\n".join(text)

    def column(self, name):
        return self.columns[name]
