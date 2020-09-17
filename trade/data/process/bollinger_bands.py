from .moving_average import MovingAverage
from .moving_std import MovingStd


class BollingerBands(object):
    def __init__(self, window):
        self.window = int(window)

    def process(self, df):
        ma_df = MovingAverage(self.window).process(df)
        ms_df = MovingStd(self.window).process(df)
        return (ma_df + ms_df * 2, ma_df - ms_df * 2)
