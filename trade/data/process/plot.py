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
        self.plotter.plot(column.name, column.data)


class StockPlotter(object):
    def __init__(self, plotters, stock):
        self.plotters = plotters
        self.stock = stock

    def plot(self, present):
        for plotter in self.plotters:
            plotter.set_present(present)
            Plot(plotter).process(self.stock)


class ScreenPlot(column_base.ColumnBase):
    def __init__(self, plotters):
        self.plotters = plotters

    def plot(self):
        for plotter in self.plotters:
            plotter.plot(_ScreenPresent())


class PdfPlot(object):
    def __init__(self, plotters, plot_path):
        self.plotters = plotters
        self.plot_path = plot_path

    def plot(self):
        with PdfPages(self.plot_path) as pdf:
            for plotter in self.plotters:
                plotter.plot(_PdfPresent(pdf))


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
    def __init__(self, baseline=None, bins=20):
        super(Histogram, self).__init__()
        self.bins = bins
        self.baseline = baseline

    def plot(self, name, df):
        bl = self.baseline or df.columns[0]

        _, ax = plt.subplots()

        bl_h, bl_bins = np.histogram(df[bl], bins=self.bins)
        width = (bl_bins[1] - bl_bins[0]) / len(df.columns)

        ax.bar(bl_bins[:-1], bl_h, width=width, label=bl)

        count = 1
        for ticker in df.columns:
            if ticker == bl:
                continue
            h, bins = np.histogram(df[ticker], bins=bl_bins)
            ax.bar(bins[:-1] + (width*count), h, width=width, label=ticker)
            count += 1

        mean = df[bl].mean()
        std = df[bl].std()

        plt.axvline(mean, color='black', linestyle='dashed', linewidth=2)
        plt.axvline(mean+std, color='r', linestyle='dashed', linewidth=2)
        plt.axvline(mean-std, color='r', linestyle='dashed', linewidth=2)
        plt.title("avg={} std={}".format(mean, std))

        plt.legend(loc='upper right')
        self.present()


class Scatter(Plotter):
    def __init__(self, baseline, learner=utils.LinRegLearner()):
        super(Scatter, self).__init__()
        self.baseline = baseline
        self.learner = learner

    def plot(self, name, df):
        if self.baseline not in df.columns:
            raise ValueError(
                "No {} ticker in {} column".format(
                    self.baseline, name))

        for ticker in df.columns:
            if ticker == self.baseline:
                continue

            df.plot(kind='scatter', x=self.baseline, y=ticker)

            b, a = np.polyfit(df[self.baseline], df[ticker], 1)

            self.learner.train(df[self.baseline], df[ticker])
            plt.plot(df[self.baseline], self.learner.query(
                df[self.baseline]), '-', color='r')
            plt.title("alpha={} beta={}".format(self.learner.m, self.learner.b))
            self.present()
