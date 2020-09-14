import argparse
import datetime
import pandas as pd
import numpy as np
import scipy.optimize as spo
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from trade.data import (Column, reader, process)
import trade.type


class SuperEnsembleLerner:
    def __init__(
            self,
            gbr=False,
            rfr=False,
            mlpr=False,
            lr=False,
            svr=False,
            dtr=False,
            knr=False):
        self.learners = ()
        # ok
        if gbr:
            self.learners = self.learners + \
                (GradientBoostingRegressor(learning_rate=0.1, n_estimators=100),)

        # ok
        if rfr:
            self.learners = self.learners + \
                (RandomForestRegressor(n_estimators=100),)

        # so so
        if mlpr:
            self.learners = self.learners + (
                AdaBoostRegressor(
                    base_estimator=MLPRegressor(
                        hidden_layer_sizes=(
                            80, 30,)), n_estimators=300),)

        # so so
        if lr:
            self.learners = self.learners + \
                (AdaBoostRegressor(base_estimator=LinearRegression(), n_estimators=100),)

        # bad
        if svr:
            self.learners = self.learners + \
                (AdaBoostRegressor(base_estimator=SVR(degree=10)),)

        # bad
        if dtr:
            self.learners = self.learners + \
                (AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),)

        # ?
        if knr:
            self.learners = self.learners + \
                (AdaBoostRegressor(base_estimator=KNeighborsRegressor()),)

    def fit(self, X, y):
        for learner in self.learners:
            learner.fit(X, y)
            # print learner.feature_importances_

    def predict(self, X):
        pred = ()
        for learner in self.learners:
            pred = pred + (learner.predict(X),)

        return np.mean(pred, axis=0)


# def prepare_input(df, window, predict):
#     momentum = utils.compute_momentum(df, window)
#     ma = utils.compute_moving_avg(df, window)
#     maq = utils.compute_moving_avg(df, window / 4)
#     ma_hist = maq - ma
#
#     ms = utils.compute_moving_std(df, window)
#
#     emal = utils.compute_exp_moving_avg(df, window)
#     emas = utils.compute_exp_moving_avg(df, window / 2)
#     emad = emas - emal
#     macd = utils.compute_exp_moving_avg(emad, window / 3)
#     macd_hist = emad - macd
#
#     rs = utils.compute_reletive_strength(df, window)
#
#     res = momentum.join(
#         ma_hist,
#         rsuffix='_moving_avg_hist').join(
#         ms,
#         rsuffix='_moving_std').join(
#         macd_hist,
#         rsuffix='_macd_hist').join(
#         rs,
#         rsuffix="_rs")
#     res = res[window:-predict]
#     res = (res - res.mean()) / res.std()
#     return res
#
#
# def compute_prediction(df, predict):
#     """Compute and return the daily return values."""
#     dr = df.shift(-predict)
#     return dr
#
#
# def prepare_output(df, window, predict):
#     pred = compute_prediction(df, predict)
#     return pred[window:-predict]


def analize(tickers, start, end, baseline, window, predict, test_size):
    dates = pd.date_range(start, end)
    stock = process.ProcessLine([process.Baseline(baseline), process.FillMissing(), process.Range(
        dates)]).process(reader.CsvReader().read_stock(tickers, [Column.Name.ADJCLOSE]))

    ac_data = stock.column(Column.Name.ADJCLOSE)

#     for ticker in tickers:
#         df = ac_data.data[[ticker]]
#         learn_pool = df.shape[0] - window - predict - test_size
#
#         res = []
#         for name, learner in [
#             ("rfr+dtr+knr", SuperEnsembleLerner(rfr=True, dtr=True, knr=True)),
#             ("gbr+rfr+dtr", SuperEnsembleLerner(gbr=True, rfr=True, dtr=True)),
#         ]:
#             X = prepare_input(df, window, predict)
#             Y = prepare_output(df, window, predict)
#             X_learn = X[:learn_pool + 1]
#             Y_learn = Y[:learn_pool + 1]
#             X_test = X[learn_pool:]
#             Y_test = Y[learn_pool:]
#             learner.fit(X_learn, Y_learn)
#             test_pred = learner.predict(X_test)
#             Y_test["%s_pred-test" % (ticker)] = test_pred
#             Y_test = Y_test.rename(columns={ticker: "%s-test" % (ticker)})
#             learn_pred = learner.predict(X_learn)
#             Y_learn["%s_pred" % (ticker)] = learn_pred
#
#             res += [(name, pd.concat([Y_learn, Y_test])
#                      [-(window + predict + test_size):])]
    # utils.plot_to_pdf(ticker, res)


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-w', '--window', required=True, type=int,
                        help="Window size")
    parser.add_argument('-p', '--predict', required=True, type=int,
                        help="Prediction input size")
    parser.add_argument('-t', '--test', required=True, type=int,
                        help="Test data size")
    args = parser.parse_args()

    analize(
        args.tickers,
        args.start,
        args.end,
        args.baseline,
        args.window,
        args.predict,
        args.test)


if __name__ == "__main__":
    run()
