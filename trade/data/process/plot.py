import column_base
import numpy as np
import matplotlib.pyplot as plt
from trade import utils
from trade.data import storage


class Plot(column_base.ColumnBase):
    def __init__(self, title="Stock", xlabel="Date", ylabel="Price"):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def process_column(self, column):
        graph = column.df.plot(
            title="{}: {}".format(
                self.title,
                column.name),
            fontsize=8)
        graph.set_xlabel(self.xlabel)
        graph.set_ylabel(self.ylabel)
        plt.show()


class PlotHistogram(column_base.ColumnBase):
    def __init__(self, bins=20):
        self.bins = bins

    def process_column(self, column):
        for ticker in column.df.columns:
            column.df[ticker].hist(bins=self.bins, label=ticker)
        plt.legend(loc='upper right')
        plt.show()


class PlotScatter(column_base.ColumnBase):
    def __init__(self, base_ticker):
        self.base_ticker = base_ticker

    def process_column(self, column):
        if self.base_ticker not in column.df.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.base_ticker, column.name))

        for ticker in column.df.columns:
            if ticker == self.base_ticker:
                continue
            column.df.plot(kind='scatter', x=self.base_ticker, y=ticker)
            b, a = np.polyfit(
                column.df[self.base_ticker], column.df[ticker], 1)
            lgl = utils.LinRegLearner()
            lgl.train(column.df[self.base_ticker], column.df[ticker])
            plt.plot(column.df[self.base_ticker], lgl.query(
                column.df[self.base_ticker]), '-', color='r')
            plt.show()
