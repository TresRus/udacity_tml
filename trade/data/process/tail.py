class Tail(object):
    def __init__(self, length):
        self.length = length

    def process(self, df):
        return df[-self.length:]
