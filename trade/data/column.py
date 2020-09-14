import pandas as pd
from enum import Enum


class Column(object):
    class Name(object):
        DATE = "Date"
        ADJCLOSE = "Adj Close"
        CLOSE = "Close"
        HIGH = "High"
        LOW = "Low"
        OPEN = "Open"
        VOLUME = "Volume"

    def __init__(self, name):
        self.name = name
        self.data = pd.DataFrame()

    def __str__(self):
        return str(self.data)
