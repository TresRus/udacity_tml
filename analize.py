import load
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

    ubb = ma + ms * 2
    lbb = ma - ms * 2

    res = daily_ret.join(
        momentum,
        rsuffix='_momentum').join(
            ma,
            rsuffix='_moving_avg').join(
                ubb,
                rsuffix='_upper_bb').join(
                    lbb,
        rsuffix='_lower_bb')
    res = (res - res.mean()) / res.std()
    return res[window:-predict]


def prepare_output(df, window, predict):
    pred = utils.compute_prediction(df, predict)
    return pred[window:-predict]


def main():
    currencies = {
        #'USDT': 'tether',
        'ETH': 'ethereum',
        'XRP': 'ripple',
        'NEO': 'neo',
        'XVG': 'verge',
        # 'ICX': 'icon'
    }

    horizon = 200
    learn_pool = 160
    window = 20
    predict = 5

    data_start = datetime.date(2009, 1, 1)
    data_end = datetime.datetime.now() - datetime.timedelta(days=1)

    df_start = data_end - datetime.timedelta(days=horizon)
    df_end = data_end

    learn_start = data_end - datetime.timedelta(days=horizon)
    learn_end = learn_start + datetime.timedelta(days=learn_pool)

    test_start = data_end - datetime.timedelta(days=horizon - learn_pool)
    test_end = data_end

    # load.load_dict(currencies, data_start, data_end)

    dates = pd.date_range(
        df_start.strftime('%Y-%m-%d'),
        df_end.strftime('%Y-%m-%d'))
    df = utils.get_data(currencies.keys(), dates, 'cc_data')
    utils.fill_missing_values(df)
    ndf = utils.normolize(df)

    """
    full_df = prepare_data(ndf, window, predict)
    learn_ndf = full_df[:learn_pool+1]
    test_ndf = full_df[learn_pool:]

    test_rename = {}
    for name in currencies.keys():
        test_rename[name] = "%s-test" % (name)
    test_ndf = test_ndf.rename(columns=test_rename)
    """

    for name in currencies.keys():
        X = prepare_input(ndf[[name]], window, predict)
        Y = prepare_output(ndf[[name]], window, predict)
        X_learn = X[:learn_pool + 1]
        Y_learn = Y[:learn_pool + 1]
        X_test = X[learn_pool:]
        Y_test = Y[learn_pool:]
        # plot_info(ndf[[name]], window)
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


if __name__ == "__main__":
    main()
