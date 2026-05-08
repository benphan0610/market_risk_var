import pandas as pd
import numpy as np
import yfinance as yf

from src.config import SAMPLE_START, SAMPLE_END, MIN_HISTORY_DAYS


def download_prices(tickers):
    data = yf.download(tickers, start = SAMPLE_START, end = SAMPLE_END, progress = False)
    return data["Close"]

def compute_returns(prices):
    return np.log(prices / prices.shift(1)).dropna(how="all")

def filter_tickers(returns):
    return returns.dropna(axis = 1, thresh = MIN_HISTORY_DAYS)

def build_portfolio(returns):
    return returns.mean(axis = 1).rename("return")

def save_panel(df, path):
    df.index.name = "date"
    df.to_csv(path, index = True)
    
def read_panel(path):
    return pd.read_csv(path, parse_dates = ["date"], index_col = "date")
    