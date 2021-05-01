from sklearn.linear_model import LinearRegression
import numpy as np


def LinearRegression_func(X, y):
    X = X.reshape(-1, 1)
    # print("Linear Regression:")
    # print("X:\n" + str(X))
    # print("y: " + str(y))
    reg = LinearRegression()
    reg.fit(X, y)
    # print("score: " + str(reg.score(X, y)))
    # print("thetas: " + str(reg.coef_))
    # print("intercept: " + str(reg.intercept_))
    return reg.coef_[0], reg.score(X, y)
