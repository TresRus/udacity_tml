import scipy.stats as sps


class LinRegLearner:
    def __init__(self):
        pass

    def train(self, X, Y):
        self.m, self.b, _, _, _ = sps.linregress(X, Y)

    def query(self, X):
        Y = self.m * X + self.b
        return Y
