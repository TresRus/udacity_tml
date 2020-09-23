from .moving_average import MovingAverage

class SMA(object):
    def __init__(self, window):
        self.window = window

    def process(self, df):
        return (df / MovingAverage(self.window).process(df)) - 1.
