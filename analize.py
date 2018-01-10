import load
import datetime
import pandas as pd
import numpy as np
import scipy.optimize as spo
import utils
import sklearn


def reverse_sr(allocates, df):
    return utils.sharpe_ratio(utils.portfolio_val(df, allocates), utils.daily_free_risk()) * -1;

def sum_one(allocates):
    return np.sum(allocates) - 1.0

def fit_line(df, error_func):
    column_num = df.shape[1]
    init_allocates = np.ones(column_num) / column_num

    limits = ()
    for x in range(column_num):
        limits += ((0.0, 1.0),)

    constr = {'type':'eq', 'fun':sum_one}

    result = spo.minimize(error_func, init_allocates, args=(df,), method='SLSQP', bounds=limits, constraints=constr, options={'disp': True})
    return result.x


class SuperEnsembleLerner:
    def __init__(self):
        self.lerners = ()
        self.lerners = self.lerners + (sklearn.ensemble.GradientBoostingRegressor(),)
        self.lerners = self.lerners + (sklearn.ensemble.RandomForestRegressor(),)
        self.lerners = self.lerners + (sklearn.ensemble.AdaBoostRegressor(base_estimator=sklearn.neural_network.MLPRegressor),)
        self.lerners = self.lerners + (sklearn.ensemble.AdaBoostRegressor(base_estimator=sklearn.svr.SVR),)
        self.lerners = self.lerners + (sklearn.ensemble.AdaBoostRegressor(base_estimator=sklearn.tree.DecisionTreeRegressor),)
        self.lerners = self.lerners + (sklearn.ensemble.AdaBoostRegressor(base_estimator=sklearn.neighbors.KNeighborsRegressor),)
        self.lerners = self.lerners + (sklearn.ensemble.AdaBoostRegressor(base_estimator=sklearn.linear_model.LinearRegression),)

    def fit(self, X, y):
        for learner in self.learners:
            learner.fit(X, y)

    def predict(self, X):
        pred = ()
        for learner in self.learners:
            pred = pred + (learner.predict(X),)

        return np.mean(pred)


def main():
    currencies = {
        'USDT': 'tether',
        'ETH': 'ethereum',
        'XRP': 'ripple',
        'NEO': 'neo',
        'XVG': 'verge',
        'ICX': 'icon'
    }

    horizon = 300
    learn_pool = 200
    window = 40
    predict = 10

    data_start = datetime.date(2009, 1, 1)
    data_end = datetime.datetime.now()

    df_start = data_end - datetime.timedelta(days=horizon)
    df_end = data_end

    learn_start = data_end - datetime.timedelta(days=horizon)
    learn_end = learn_start + datetime.timedelta(days=learn_pool)

    test_start = data_end - datetime.timedelta(days=horizon-learn_pool)
    test_end = data_end

    # load.load_dict(currencies, data_start, data_end)

    dates = pd.date_range(df_start.strftime('%Y-%m-%d'), df_end.strftime('%Y-%m-%d'))
    df = utils.get_data(currencies.keys(), dates, 'cc_data')
    utils.fill_missing_values(df)
    ndf = utils.normolize(df)

    learn_ndf = ndf[:learn_pool+1]
    test_ndf = ndf[learn_pool:]

    test_rename = {}
    for name in currencies.keys():
        test_rename[name] = "%s-test" % (name)
    test_ndf = test_ndf.rename(columns=test_rename)

    res_df = pd.concat([learn_ndf, test_ndf])
    utils.plot_data(res_df)

    daily_ret = utils.compute_daily_returns(res_df)
    utils.plot_data(daily_ret)

if __name__ == "__main__":
    main()
