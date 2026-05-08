import numpy as np
import pandas as pd

from src.var_methods import (
    historical_var, normal_var, student_t_var, monte_carlo_var, compute_all_static,
)

def test_historical_var_known_quantile():
    returns = np.linspace(-0.05, 0.05, 1000)
    var, es = historical_var(returns, 0.95)
    assert np.isclose(var, 0.045, atol = 0.001)
    assert es > var
    
def test_normal_var_matches_formula():
    np.random.seed(0)
    returns = np.random.randn(1000) * 0.01
    var, es = normal_var(returns, 0.95)
    assert np.isclose(var, 0.0165, atol = 0.02)
    assert es > var
    
def test_var_methods_return_postitive_var():
    np.random.seed(42)
    returns = np.random.randn(500) * 0.012 - 0.0005
    
    for method in [historical_var, normal_var, student_t_var, monte_carlo_var]:
        var, es = method(returns, 0.95)
        assert var > 0, f"{method.__name__} returned non-positive VaR"
        assert es > 0, f"{method.__name__} returned non-positive ES"
        assert es >= var, f"{method.__name__} returned ES < VaR"
        
def test_es_is_sign_consistent():
    np.random.seed(0)
    returns = np.random.randn(1000) * 0.01
            
    for method in [historical_var, normal_var, student_t_var, monte_carlo_var]:
        var, es = method(returns, 0.95)
        assert es > 0, f"{method.__name__} returned negative ES"
        
def test_compute_all_static_shape():
    np.random.seed(0)
    n_days = 500
    returns = pd.Series(
        np.random.rand(n_days) * 0.01,
        index = pd.date_range("2020-01-01", periods = n_days, freq = "B"),
    )        
    
    result = compute_all_static(returns, level = 0.95, window = 100)
    assert result.shape == (n_days - 100, 8)
    assert "historical_var" in result.columns
    assert "normal_es" in result.columns
        
    
    