import pandas as pd
import numpy as np
import yfinance as yf

from src.config import SAMPLE_START, SAMPLE_END, MIN_HISTORY_DAYS


# Pull data from yfinance
def download_prices(tickers):
    data = yf.download(tickers, start = SAMPLE_START, end = SAMPLE_END, progress = False)
    return data["Close"]

# Calculate the log returns and drop all NaN
def compute_returns(prices):
    return np.log(prices / prices.shift(1)).dropna(how="all")

# Drop tickers that don't have at least MIN_HISTORY_DAYS non-NaN observations
def filter_tickers(returns):
    return returns.dropna(axis = 1, thresh = MIN_HISTORY_DAYS)

# Equal-weighted portfolio with daily rebalancing
def build_portfolio(returns):
    return returns.mean(axis = 1).rename("return")

# Saved to Parquet files
def save_panel(df, path):
    df.index.name = "date"
    df.to_parquet(path)
    
# Read Parquet files
def read_panel(path):
    return pd.read_parquet(path)
    