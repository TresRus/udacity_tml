import numpy as np
import pandas as pd
import os
import math


def compute_momentum(df, window):
    dr = (df - df.shift(window))
    dr.ix[0:window, :] = 0
    return dr


def compute_moving_avg(df, window):
    dr = df.rolling(window).mean()
    dr.ix[0:window, :] = df.ix[0:window, :]
    return dr


def compute_exp_moving_avg(df, window):
    dr = df.ewm(span=window).mean()
    dr.ix[0:window, :] = df.ix[0:window, :]
    return dr


def compute_moving_std(df, window):
    dr = df.rolling(window).std()
    dr.ix[0:window, :] = 0
    return dr


def compute_reletive_strength(df, window):
    delta = df.diff()

    up = delta.copy()
    up[up < 0] = 0

    down = delta.copy()
    down[down > 0] = 0

    ru = up.ewm(span=window).mean().abs()
    rd = down.ewm(span=window).mean().abs()

    res = ru / rd
    res.fillna(method='ffill', inplace=True)

    return res


def compute_prediction(df, predict):
    """Compute and return the daily return values."""
    dr = df.shift(-predict)
    return dr


def reverse_sr(allocates, mdp):
    return sharpe_ratio(mdp.portfolio_val(allocates),
                        daily_free_risk()) * -1


def count_betas(df, symbols, base):
    res = ()
    for symbol in symbols:
        if symbol == base:
            continue
        df.plot(kind='scatter', x=base, y=symbol)
        b, a = np.polyfit(df[base], df[symbol], 1)
        res = res + (b,)
    return res
