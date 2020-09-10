import column_base
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from trade import utils


class _ScreenPresent(object):
    def __call__(self):
        plt.show()


class _PdfPresent(object):
    def __init__(self, pdf):
        self.pdf = pdf

    def __call__(self):
        self.pdf.savefig()
        plt.close()


class Plot(column_base.ColumnBase):
    def __init__(self, plotter):
        self.plotter = plotter

    def process_column(self, column):
        self.plotter.plot(column.name, column.df)


class PdfPlotter(object):
    def __init__(self, plotters, stock):
        self.plotters = plotters
        self.stock = stock

    def plot(self, pdf):
        for plotter in self.plotters:
            plotter.set_present(_PdfPresent(pdf))
            Plot(plotter).process(self.stock)


class MultyplotPdf(object):
    def __init__(self, pdf_plotters, plot_path):
        self.pdf_plotters = pdf_plotters
        self.plot_path = plot_path

    def plot(self):
        with PdfPages(self.plot_path) as pdf:
            for pdf_plotter in self.pdf_plotters:
                pdf_plotter.plot(pdf)


class PlotPdf(object):
    def __init__(self, plotters, plot_path):
        self.plotters = plotters
        self.plot_path = plot_path

    def process(self, stock):
        with PdfPages(self.plot_path) as pdf:
            for plotter in self.plotters:
                plotter.set_present(_PdfPresent(pdf))
                Plot(plotter).process(stock)


class Plotter(object):
    def __init__(self):
        self.present = _ScreenPresent()

    def set_present(self, present):
        self.present = present


class Graph(Plotter):
    def __init__(self, title="Stock", xlabel="Date", ylabel="Price"):
        super(Graph, self).__init__()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot(self, name, df):
        graph = df.plot(title="{}: {}".format(self.title, name), fontsize=8)
        graph.set_xlabel(self.xlabel)
        graph.set_ylabel(self.ylabel)
        self.present()


class Histogram(Plotter):
    def __init__(self, bins=20):
        super(Histogram, self).__init__()
        self.bins = bins

    def plot(self, name, df):
        for ticker in df.columns:
            df[ticker].hist(bins=self.bins, label=ticker)
        plt.legend(loc='upper right')
        self.present()


class Scatter(Plotter):
    def __init__(self, base_ticker):
        super(Scatter, self).__init__()
        self.base_ticker = base_ticker

    def plot(self, name, df):
        if self.base_ticker not in df.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.base_ticker, name))

        for ticker in df.columns:
            if ticker == self.base_ticker:
                continue
            df.plot(kind='scatter', x=self.base_ticker, y=ticker)
            b, a = np.polyfit(df[self.base_ticker], df[ticker], 1)
            lgl = utils.LinRegLearner()
            lgl.train(df[self.base_ticker], df[ticker])
            plt.plot(df[self.base_ticker], lgl.query(
                df[self.base_ticker]), '-', color='r')
            self.present()
