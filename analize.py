import argparse
import datetime
import pandas as pd
import numpy as np
import scipy.optimize as spo
import utils
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression


class SuperEnsembleLerner:
    def __init__(self, gbr=False, rfr=False, mlpr=False, lr=False, svr=False, dtr=False, knr=False):
        self.learners = ()
        # ok
        if gbr:
            self.learners = self.learners + \
                (GradientBoostingRegressor(learning_rate=0.1, n_estimators=100),)

        # ok
        if rfr:
            self.learners = self.learners + (RandomForestRegressor(n_estimators=100),)

        # so so
        if mlpr:
            self.learners = self.learners + \
                (AdaBoostRegressor(base_estimator=MLPRegressor(hidden_layer_sizes=(80, 30,)), n_estimators=300),)

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


def plot_info(name, df, window):
    ma = utils.compute_moving_avg(df, window)
    mah = utils.compute_moving_avg(df, window / 2)
    maq = utils.compute_moving_avg(df, window / 4)

    ms = utils.compute_moving_std(df, window)
    ubb = ma + ms * 2
    lbb = ma - ms * 2

    emal = utils.compute_exp_moving_avg(df, window)
    emas = utils.compute_exp_moving_avg(df, window / 2)
    emad = emas - emal
    macd = utils.compute_exp_moving_avg(emad, window / 3)

    rs = utils.compute_reletive_strength(df, window)
    rsi = 100 - 100 / (1 + rs)

    r1 = df.join(
        ma,
        rsuffix='_moving_avg').join(
        ubb,
        rsuffix='_upper_bb').join(
        lbb,
        rsuffix='_lower_bb')
    r2 = df.join(
        mah,
        rsuffix='_moving_avg_h').join(
        maq,
        rsuffix='_moving_avg_q')
    r3 = emad.join(
        macd,
        rsuffix='_macd')
    r4 = rsi
    plot_num = window * 2
    utils.plot_to_pdf(name,
                      [ ("Average+boundries", r1[-plot_num:]),
                        ("Averages", r2[-plot_num:],),
                        ("MACD", r3[-plot_num:]),
                        ("RSI", r4[-plot_num:]) ])


def prepare_input(df, window, predict):
    momentum = utils.compute_momentum(df, window)
    ma = utils.compute_moving_avg(df, window)
    maq = utils.compute_moving_avg(df, window / 4)
    ma_hist = maq - ma

    ms = utils.compute_moving_std(df, window)

    emal = utils.compute_exp_moving_avg(df, window)
    emas = utils.compute_exp_moving_avg(df, window / 2)
    emad = emas - emal
    macd = utils.compute_exp_moving_avg(emad, window / 3)
    macd_hist = emad - macd

    rs = utils.compute_reletive_strength(df, window)

    res = momentum.join(
        ma_hist,
        rsuffix='_moving_avg_hist').join(
        ms,
        rsuffix='_moving_std').join(
        macd_hist,
        rsuffix='_macd_hist').join(
        rs,
        rsuffix="_rs")
    res = res[window:-predict]
    # utils.plot_data(res)
    res = (res - res.mean()) / res.std()
    # utils.plot_data(res)
    return res


def prepare_output(df, window, predict):
    pred = utils.compute_prediction(df, predict)
    return pred[window:-predict]


def get_market_data(dates):
    load_currencies = json.load(open('top100.json'))
    load_params = ['Close', 'Market Cap']

    all_data = utils.get_data(
        load_currencies.keys(),
        load_params,
        dates,
        'cc_data')
    for _, stock in all_data.iteritems():
        utils.fill_missing_values(stock)

    mc = all_data['Market Cap'].df
    mc = mc / mc.sum()

    price = all_data['Close'].df * mc
    return price.sum(axis=1).to_frame(name='Market')


def analize(tickers, start, end, window, predict, test_size):
    dates = pd.date_range(start, end)
    md = utils.data.Market(dates, utils.data.CsvReader())
    md.load(tickers, [utils.data.Column.Name.ADJCLOSE])
    ac_data = md.column(utils.data.Column.Name.ADJCLOSE)

    ac_data.load_snp_baseline()
    ac_data.load_tickers(tickers)
    ac_data.fill_missing_values()

    for ticker in tickers:
        df = ac_data.df[[ticker]]
        plot_info(ticker, df, window)

        learn_pool = df.shape[0] - window - predict - test_size

        res = []
        for name, learner in [
                               ("rfr+dtr+knr", SuperEnsembleLerner(rfr=True, dtr=True, knr=True)),
                               ("gbr+rfr+dtr", SuperEnsembleLerner(gbr=True, rfr=True, dtr=True)),
                               ]:
            X = prepare_input(df, window, predict)
            Y = prepare_output(df, window, predict)
            X_learn = X[:learn_pool + 1]
            Y_learn = Y[:learn_pool + 1]
            X_test = X[learn_pool:]
            Y_test = Y[learn_pool:]
            learner.fit(X_learn, Y_learn)
            test_pred = learner.predict(X_test)
            Y_test["%s_pred-test" % (ticker)] = test_pred
            Y_test = Y_test.rename(columns={ ticker: "%s-test" % (ticker) })
            learn_pred = learner.predict(X_learn)
            Y_learn["%s_pred" % (ticker)] = learn_pred

            res += [ (name, pd.concat([Y_learn, Y_test])[-(window+predict+test_size):]) ]
        utils.plot_to_pdf(ticker, res)



def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-s', '--start', required=True, type=utils.date_arg,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=utils.date_arg,
                        help="Evaluation end date")
    parser.add_argument('-w', '--window', required=True, type=int,
                        help="Window size")
    parser.add_argument('-p', '--predict', required=True, type=int,
                        help="Prediction input size")
    parser.add_argument('-t', '--test', required=True, type=int,
                        help="Test data size")
    args = parser.parse_args()

    analize(args.tickers, args.start, args.end, args.window, args.predict, args.test)


if __name__ == "__main__":
    run()
