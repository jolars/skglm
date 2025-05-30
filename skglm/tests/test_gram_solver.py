import pytest
from itertools import product

import numpy as np
from numpy.linalg import norm
from sklearn.linear_model import Lasso

from skglm.penalties import L1
from skglm.solvers import GramCD

from skglm.utils.data import make_correlated_data


@pytest.mark.parametrize("rho, X_density, greedy_cd",
                         product([1e-1, 1e-3], [1., 0.8], [True, False]))
def test_vs_lasso_sklearn(rho, X_density, greedy_cd):
    X, y, _ = make_correlated_data(
        n_samples=18, n_features=8, random_state=0, X_density=X_density)
    alpha_max = norm(X.T @ y, ord=np.inf) / len(y)
    alpha = rho * alpha_max

    sk_lasso = Lasso(alpha, fit_intercept=False, tol=1e-9)
    sk_lasso.fit(X, y)

    l1_penalty = L1(alpha)
    w = GramCD(tol=1e-9, max_iter=1000, greedy_cd=greedy_cd).solve(
        X, y, None, l1_penalty)[0]
    np.testing.assert_allclose(w, sk_lasso.coef_.flatten(), rtol=1e-7, atol=1e-7)


if __name__ == '__main__':
    pass
