import datetime
import pandas as pd
import numpy as np
import scipy.optimize as spo
import utils
import json
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression


class SuperEnsembleLerner:
    def __init__(self):
        self.learners = ()
        # ok
        self.learners = self.learners + \
            (GradientBoostingRegressor(learning_rate=0.1, n_estimators=100),)

        # ok
        #self.learners = self.learners + (RandomForestRegressor(n_estimators=100),)

        # so so
        # self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=MLPRegressor(hidden_layer_sizes=(80, 30,)), n_estimators=300),)

        # so so
        # self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=LinearRegression(), n_estimators=100),)

        # bad
        # self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=SVR(degree=10)),)

        # bad
        # self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),)

        # ?
        # self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=KNeighborsRegressor()),)

    def fit(self, X, y):
        for learner in self.learners:
            learner.fit(X, y)
            print learner.feature_importances_

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
                      (r1[-plot_num:],
                       r2[-plot_num:],
                          r3[-plot_num:],
                          r4[-plot_num:]))


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
    utils.plot_data(res)
    res = (res - res.mean()) / res.std()
    utils.plot_data(res)
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


def main():
    analize_currencies = [
        'ETH',
        'XRP',
        'NEO',
        'XVG',
        'GNT',
        'XRB',
        'ADA',
        'XEM',
        'XMR']
    # analize_currencies = json.load(open('top100.json'))
    analize_params = ['Close']

    horizon = 300
    learn_pool = 250
    window = 30
    predict = 7

    data_start = datetime.date(2009, 1, 1)
    data_end = datetime.datetime.now() - datetime.timedelta(days=1)

    df_start = data_end - datetime.timedelta(days=horizon)
    df_end = data_end

    dates = pd.date_range(
        df_start.strftime('%Y-%m-%d'),
        df_end.strftime('%Y-%m-%d'))

    market = get_market_data(dates)
    n_market = utils.normalize(market)

    md = utils.MarketData(dates, data_dir='cc_data')
    md.get_data(analize_currencies, analize_params)
    for _, stock in md.data.iteritems():
        stock.fill_missing_values()
    stocks = md.data['Close']
    n_stocks = stocks.normalize()

    """
    full = stocks.join(market)
    n_full = utils.normalize(full[:window])
    utils.plot_data(n_full)
    utils.plot_data(utils.compute_daily_returns(n_full))
    """

    for name in analize_currencies:
        plot_info(name, stocks[[name]], window)

        """
        X = prepare_input(stocks[[name]], window, predict)
        Y = prepare_output(stocks[[name]], window, predict)
        X_learn = X[:learn_pool + 1]
        Y_learn = Y[:learn_pool + 1]
        X_test = X[learn_pool:]
        Y_test = Y[learn_pool:]
        learner = SuperEnsembleLerner()
        learner.fit(X_learn, Y_learn)
        test_pred = learner.predict(X_test)
        Y_test["%s_pred-test" % (name)] = test_pred
        Y_test = Y_test.rename(columns={ name: "%s-test" % (name) })
        learn_pred = learner.predict(X_learn)
        Y_learn["%s_pred" % (name)] = learn_pred

        res = pd.concat([Y_learn, Y_test])
        utils.plot_data(res)
        """


if __name__ == "__main__":
    main()
