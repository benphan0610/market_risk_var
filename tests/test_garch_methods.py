import numpy as np
import pandas as pd
from src.garch_methods import garch_forecasts

def make_fake_returns(n_days = 600, seed = 0):
    np.random.seed(seed)
    dates = pd.date_range("2020-01-01", periods = n_days, freq = "B")
    returns = np.random.randn(n_days) * 1.0 - 0.05
    return pd.Series(returns, index = dates)

def test_garch_output_shape():
    returns = make_fake_returns(n_days = 600)
    result = garch_forecasts(returns, asymmetric = False)
    
    assert (result["forecast_vol"] > 0).all()
    
def test_garch_forecasts_are_reasonable_magnitude():
    returns = make_fake_returns(n_days = 600)
    result = garch_forecasts(returns, asymmetric = False)
    
    mean_vol = result["forecast_vol"].mean()
    assert 0.5 < mean_vol < 2.0, f"Expected vol near 1, got {mean_vol:.3f}"
    
def test_gjr_differs_from_garch():
    returns = make_fake_returns(n_days = 600)
    
    garch_result = garch_forecasts(returns, asymmetric = False)
    gjr_result = garch_forecasts(returns, asymmetric = True)
    
    diff = (garch_result["forecast_vol"] - gjr_result["forecast_vol"]).abs().sum()
    assert diff > 0, "GJR and GARCH produced identical forecasts"