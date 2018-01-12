import load
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
        self.learners = self.learners + (GradientBoostingRegressor(learning_rate=0.05, n_estimators=100),)

        # ok
        self.learners = self.learners + (RandomForestRegressor(n_estimators=100),)

        # so so
        self.learners = self.learners + \
            (AdaBoostRegressor(base_estimator=MLPRegressor(hidden_layer_sizes=(80, 30,)), n_estimators=300),)

        # so so
        self.learners = self.learners + \
            (AdaBoostRegressor(base_estimator=LinearRegression(), n_estimators=100),)

        # bad
        #self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=SVR(degree=10)),)

        # bad
        #self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),)

        # ?
        #self.learners = self.learners + \
        #    (AdaBoostRegressor(base_estimator=KNeighborsRegressor()),)

    def fit(self, X, y):
        for learner in self.learners:
            learner.fit(X, y)

    def predict(self, X):
        pred = ()
        for learner in self.learners:
            pred = pred + (learner.predict(X),)

        return np.mean(pred, axis=0)

    def print_params(self):
        for learner in self.learners:
            print learner.get_params()
            print learner.feature_importances_


def plot_info(ndf, window):
    daily_ret = utils.compute_daily_returns(ndf) * ndf.mean()

    momentum = utils.compute_momentum(ndf, window)
    ma = utils.compute_moving_avg(ndf, window)
    ms = utils.compute_moving_std(ndf, window)
    ubb = ma + ms * 2
    lbb = ma - ms * 2

    res = ndf.join(
        daily_ret,
        rsuffix='_return').join(
        momentum,
        rsuffix='_momentum').join(
            ma,
            rsuffix='_moving_avg').join(
                ubb,
                rsuffix='_upper_bb').join(
                    lbb,
                    rsuffix='_lower_bb')
    utils.plot_data(res)


def prepare_input(df, window, predict):
    daily_ret = utils.compute_daily_returns(df)
    momentum = utils.compute_momentum(df, window)
    ma = utils.compute_moving_avg(df, window)
    ms = utils.compute_moving_std(df, window)

    res = daily_ret.join(
        momentum,
        rsuffix='_momentum').join(
            ma,
            rsuffix='_moving_avg').join(
                ms,
                rsuffix='_moving_std')
    res = (res - res.mean()) / res.std()
    return res[window:-predict]


def prepare_output(df, window, predict):
    pred = utils.compute_prediction(df, predict)
    return pred[window:-predict]


def main():
    load_currencies = json.load(open('top100.json'))
    load_params = ['Close', 'Market Cap']

    analize_currencies = ['ETH', 'XRP', 'NEO', 'XVG']
    # analize_currencies = ['ETH']
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

    all_data = utils.get_data(load_currencies.keys(), load_params, dates, 'cc_data')
    for _, stock in all_data.iteritems():
        utils.fill_missing_values(stock)

    mc = all_data['Market Cap']
    mc = mc / mc.sum()

    price = all_data['Close'] * mc
    market = price.sum(axis=1).to_frame(name='Market')
    n_market = utils.normolize(market)
    n_prices = utils.normolize(all_data['Close'])

    data = utils.get_data(analize_currencies, analize_params, dates, 'cc_data')
    for _, stock in data.iteritems():
        utils.fill_missing_values(stock)
    n_stocks = utils.normolize(data['Close'])

    n_full = n_stocks.join(n_market)
    n_full = utils.normolize(n_full[:30])
    # utils.plot_data(n_full)
    # n_nm = n_full.sub(n_full['Market'], axis=0)
    # utils.plot_data(n_nm)
    dr_full = utils.compute_daily_returns(n_full)
    betas = utils.count_betas(dr_full, analize_currencies, 'Market')

    print dr_full.corr(method='pearson')

    return

    """
    full_df = prepare_data(ndf, window, predict)
    learn_ndf = full_df[:learn_pool+1]
    test_ndf = full_df[learn_pool:]

    test_rename = {}
    for name in analize_currencies:
        test_rename[name] = "%s-test" % (name)
    test_ndf = test_ndf.rename(columns=test_rename)
    """

    for name in analize_currencies:
        # plot_info(ndf[[name]], window)
        X = prepare_input(ndf[[name]], window, predict)
        utils.plot_data(X)

        """
        X = prepare_input(ndf[[name]], window, predict)
        Y = prepare_output(ndf[[name]], window, predict)
        X_learn = X[:learn_pool + 1]
        Y_learn = Y[:learn_pool + 1]
        X_test = X[learn_pool:]
        Y_test = Y[learn_pool:]
        learner = SuperEnsembleLerner()
        learner.fit(X_learn, Y_learn)
        # learner.print_params()
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
