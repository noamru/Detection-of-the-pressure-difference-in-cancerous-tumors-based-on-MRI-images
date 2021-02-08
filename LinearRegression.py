from sklearn.linear_model import LinearRegression
import numpy as np


def LinearRegression_func(X, y):
    X = X.reshape(-1, 1)
    X = np.concatenate((np.array([[1]] * len(X)), X), axis=1)
    print("X:\n" + str(X))
    print("y: " + str(y))
    reg = LinearRegression()
    reg.fit(X, y)
    print("score: " + str(reg.score(X, y)))
    print("thetas: " + str(reg.coef_))
