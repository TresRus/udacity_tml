import trade.data.stock


class Statistic(object):
    def process(self, stock):
        return trade.data.stock.Statistic(stock)
