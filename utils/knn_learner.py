import scipy.stats as sps


class KNNLearner:
    def __init__(self, k):
        self.k = k

    def train(self, X, Y):
        self.x = X
        self.y = Y

    def query(self, X):
        return X
