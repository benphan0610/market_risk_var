"""Tests for data_utils."""

import pandas as pd
import numpy as np

from src.data_utils import compute_returns, filter_tickers, build_portfolio, save_panel, read_panel


def test_compute_returns_basic():
    """Log returns of doubling prices should give log(2)."""
    prices = pd.DataFrame({
        "A": [100, 200, 400],
    }, index=pd.date_range("2024-01-01", periods=3))
    returns = compute_returns(prices)
    assert np.isclose(returns["A"].iloc[0], np.log(2))


def test_filter_tickers_drops_short_history():
    """Tickers with fewer than MIN_HISTORY_DAYS observations should be dropped."""
    n_days = 2500
    full_history = np.random.randn(n_days)
    short_history = np.full(n_days, np.nan)
    short_history[:1000] = np.random.randn(1000)  # only 1000 valid obs
    
    returns = pd.DataFrame({"A": full_history, "B": short_history})
    filtered = filter_tickers(returns)
    
    assert "A" in filtered.columns
    assert "B" not in filtered.columns


def test_build_portfolio_is_cross_sectional_mean():
    """Portfolio should be the mean across tickers each day."""
    returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.03],
        "B": [0.03, 0.04, 0.05],
    }, index=pd.date_range("2024-01-01", periods=3))
    portfolio = build_portfolio(returns)
    
    assert np.isclose(portfolio.iloc[0], 0.02)  # (0.01 + 0.03) / 2
    assert np.isclose(portfolio.iloc[2], 0.04)  # (0.03 + 0.05) / 2


def test_save_and_read_round_trip(tmp_path):
    """A DataFrame saved and re-read should preserve values and dates."""
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0]},
                      index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]))
    path = tmp_path / "test.csv"
    save_panel(df, path)
    df_back = read_panel(path)
    
    assert df_back["x"].tolist() == [1.0, 2.0, 3.0]
    assert pd.api.types.is_datetime64_any_dtype(df_back.index)