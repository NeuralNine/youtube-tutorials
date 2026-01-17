import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score


class RidgeRegressionClosed:

    def __init__(self, alpha=1):
        self.coef_ = None
        self.intercept_ = 0.0
        self.alpha = alpha

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)

        Xb = np.c_[np.ones((X.shape[0], 1)), X]

        penalty_dim = Xb.shape[1]
        I = np.eye(penalty_dim)
        I[0, 0] = 0.0
        

        A = np.linalg.inv(Xb.T @ Xb + self.alpha * I) @ (Xb.T) @ y
        self.intercept_ = A[0]
        self.coef_ = A[1:]

    def predict(self, X):
        X = np.array(X)

        return X @ self.coef_ + self.intercept_



X, y = fetch_california_housing(return_X_y=True)

reg = RidgeRegressionClosed(alpha=1)
reg.fit(X, y)

y_pred = reg.predict(X)

print(r2_score(y, y_pred))


regsk = Ridge(alpha=1)
regsk.fit(X, y)

y_pred = regsk.predict(X)

print(r2_score(y, y_pred))

