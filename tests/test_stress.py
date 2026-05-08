
import numpy as np
import pandas as pd

from src.stress import compute_window_metrics


def make_test_data():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    returns = pd.Series([0.01, -0.02, -0.05, 0.01, -0.04, 0.01, 0.01, -0.06, 0.01, 0.01],
                        index=dates)
    var_series = pd.Series([0.03] * 10, index=dates)  # constant VaR
    return returns, var_series


def test_violation_count_is_correct():
    returns, var_series = make_test_data()
    metrics = compute_window_metrics(returns, var_series, "2020-01-01", "2020-01-10")
    
    # Returns below -0.03: -0.05, -0.04, -0.06 → 3 violations
    assert metrics["n_violations"] == 3


def test_worst_breach_ratio():
    returns, var_series = make_test_data()
    metrics = compute_window_metrics(returns, var_series, "2020-01-01", "2020-01-10")
    
    # Worst loss is -0.06, VaR is 0.03, so ratio is 2.0
    assert np.isclose(metrics["worst_breach_ratio"], 2.0)


def test_worst_return():
    returns, var_series = make_test_data()
    metrics = compute_window_metrics(returns, var_series, "2020-01-01", "2020-01-10")
    
    assert np.isclose(metrics["worst_return"], -0.06)


def test_no_violations_returns_zeros():
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    returns = pd.Series([0.01, 0.01, -0.01, 0.01, 0.01], index=dates)  # never below -0.03
    var_series = pd.Series([0.03] * 5, index=dates)
    
    metrics = compute_window_metrics(returns, var_series, "2020-01-01", "2020-01-05")
    
    assert metrics["n_violations"] == 0
    assert metrics["worst_breach_ratio"] == 0
    assert metrics["total_breach"] == 0