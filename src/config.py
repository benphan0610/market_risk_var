from pathlib import Path

# === Paths ===
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

# === Sample window ===
SAMPLE_START = "2010-01-01"
SAMPLE_END = "2026-01-01"

# === Tickers ===
US_TICKERS = [
    # Top 30 S&P 500 by market cap, end of 2010
    "XOM","AAPL","MSFT","COP","WMT","GOOGL","CVX","PG","IBM","JNJ",
    "JPM","WFC","ORCL","KO","C","BAC","PFE","T","GE","INTC",
    "CSCO","MRK","PEP","HD","MCD","MO","DIS","MMM","BA","CAT"
    
]

INDIA_TICKERS = [
    # Top 30 NIFTY 50 by market cap, as of 2026-04-30
    "HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","AXISBANK.NS","KOTAKBANK.NS","BAJFINANCE.NS","TCS.NS","INFY.NS","HCLTECH.NS","TECHM.NS",
    "WIPRO.NS","RELIANCE.NS","ONGC.NS","COALINDIA.NS","MARUTI.NS","M&M.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","EICHERMOT.NS","HINDUNILVR.NS",
    "ITC.NS","NESTLEIND.NS","SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS","TATASTEEL.NS","BHARTIARTL.NS","NTPC.NS","POWERGRID.NS","ASIANPAINT.NS"    
    
]

# === VaR / backtesting parameters ===
VAR_LEVELS = [0.95, 0.99]       # confidence levels run for every method
BACKTEST_WINDOW_DAYS = 252      # 252 trading days
MIN_HISTORY_DAYS = 2000         # tickers with fewer trading days get dropped


# === GARCH parameters ===
GARCH_WARMUP = 500              # initial window before first forecast
GARCH_REFIT_INTERVAL = 21       # re-fit parameters every 21 trading days

# === Monte Carlo ===
MC_N_SIMULATIONS = 10000
RANDOM_SEED = 45

# === Stress windows ===
STRESS_WINDOWS = {
    "COVID_2020": ("2020-02-15", "2020-04-15", "both"),             # gradual buildup -> sharp crash
    "CHINA_2015": ("2015-08-01", "2015-09-30", "both"),             # devaluation shock
    "Volmageddon_2018": ("2018-02-01", "2018-02-15", "US"),         # single-day shock with no buildup
}

HYPOTHETICAL_SHOCK = -0.10


