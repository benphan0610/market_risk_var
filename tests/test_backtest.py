import numpy as np
import pandas as pd

from src.backtest import (
    count_violations, kupiec_test, christoffersen_test, diebold_mariano,
)


def test_count_violations_basic():
    returns = pd.Series([0.01, -0.02, -0.05, 0.03, -0.04],
                        index = pd.date_range("2024-01-01", periods = 5))
    var = pd.Series([0.03, 0.03, 0.03, 0.03, 0.03],
                    index = pd.date_range("2024-01-01", periods = 5))
    
    violations = count_violations(returns, var)
    
    assert violations.iloc[2] == 1
    assert violations.iloc[4] == 1
    assert violations.iloc[1] == 0
    
def test_kupiec_passes_calibrated_var():
    n = 1000
    alpha = 0.05
    np.random.seed(0)
    violations = pd.Series(np.random.binomial(1, alpha, n))
    
    p_val, x, n_returned = kupiec_test(violations, alpha)
    assert n_returned == n
    assert 30 <= x <= 70
    
def test_kupiec_fails_miscalibrated_var():
    alpha = 0.05
    violations = pd.Series([1] * 200 + [0] * 800)
    
    p_val, x, n_returned = kupiec_test(violations, alpha)
    assert p_val < 0.01
    
def test_christoffersen_detects_clustering():
    violations = pd.Series([0] * 500 + [1] * 50 + [0] * 500)
    p_val = christoffersen_test(violations)
    assert p_val < 0.01
    
def test_diebold_mariano_returns_finite_values():
    np.random.seed(0)
    dates = pd.date_range("2020-01-01", periods = 500)
    returns = pd.Series(np.random.randn(500) * 0.01, index = dates)
    var_a = pd.Series(np.full(500, 0.02), index = dates)
    var_b = pd.Series(np.full(500, 0.025), index = dates)
    
    dm_stat, p_val = diebold_mariano(returns, var_a, var_b)
    assert np.isfinite(dm_stat)
    assert 0 <= p_val <= 1