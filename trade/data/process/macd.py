from .exponential_moving_average import ExponentialMovingAverage


class Macd(object):
    def __init__(self, window):
        self.window = window

    def process(self, df):
        emad = ExponentialMovingAverage(self.window).process(
            df) - ExponentialMovingAverage(self.window / 2).process(df)
        return (emad, ExponentialMovingAverage(self.window / 3).process(emad))
