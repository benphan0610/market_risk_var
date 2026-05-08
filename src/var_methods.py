import numpy as np
import pandas as pd
from scipy import stats

from src.config import BACKTEST_WINDOW_DAYS, RANDOM_SEED

def historical_var(returns_window, level):
    var = -np.quantile(returns_window, 1- level)
    bad_returns = returns_window[returns_window <= -var]
    es = -bad_returns.mean()
    return var, es

def normal_var(returns_window, level):
    mu = returns_window.mean()
    sigma = returns_window.std()
    z = stats.norm.ppf(1-level)
    var = -(mu + z*sigma)
    es = -mu + sigma*stats.norm.pdf(z)/(1-level)
    return var, es

def student_t_var(returns_window, level):
    df, loc, scale = stats.t.fit(returns_window)
    z_t = stats.t.ppf(1-level, df)
    var = -(loc + scale * z_t)
    pdf_at_z_t = stats.t.pdf(z_t, df)
    es_factor = (df + z_t**2) / (df - 1)
    es = -loc + scale * pdf_at_z_t / (1-level) * es_factor
    return var, es

def monte_carlo_var(returns_window, level, n_simulations = 10000):
    rng = np.random.default_rng(seed = RANDOM_SEED)
    simulations = rng.choice(returns_window, size = n_simulations, replace = True)
    var = -np.quantile(simulations, 1 - level)
    bad_simulations = simulations[simulations <= -var]
    es = -bad_simulations.mean()
    return var, es

def compute_all_static(returns, level, window = BACKTEST_WINDOW_DAYS):
    rows = []
    for i in range(window, len(returns)):
        win = returns.iloc[i-window:i].values
        date = returns.index[i]
        
        h_var, h_es = historical_var(win, level)
        n_var, n_es = normal_var(win, level)
        t_var, t_es = student_t_var(win, level)
        mc_var, mc_es = monte_carlo_var(win, level)
       
        rows.append({
            "date": date,
            "historical_var": h_var, "historical_es": h_es,
            "normal_var": n_var, "normal_es": n_es,
            "student_t_var": t_var, "student_t_es": t_es,
            "monte_carlo_var": mc_var, "monte_carlo_es": mc_es
        })
    return pd.DataFrame(rows).set_index("date")
