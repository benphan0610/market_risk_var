import pandas as pd
import numpy as np
from scipy import stats

def count_violations(returns, var_series):
    aligned = pd.concat([returns, var_series], axis = 1).dropna()
    aligned.columns = ["ret", "var"]
    return (aligned["ret"] < -aligned["var"]).astype(int)


def kupiec_test(violations, alpha):
    n = len(violations)
    x = violations.sum()
    p_hat = x / n
    
    if x == 0 or x == n:
        return np.nan, x, n
    
    ll_null = (n - x) * np.log(1 - alpha) + x * np.log(alpha)
    ll_alt = (n - x) * np.log(1 - p_hat) + x * np.log(p_hat)
    lr_stat = -2 * (ll_null - ll_alt)
    
    p_value = 1 - stats.chi2.cdf(lr_stat, df=1)
    return p_value, x, n


def christoffersen_test(violations):
    v = violations.values
    
    n00 = ((v[:-1] == 0) & (v[1:] == 0)).sum()
    n01 = ((v[:-1] == 0) & (v[1:] == 1)).sum()
    n10 = ((v[:-1] == 1) & (v[1:] == 0)).sum()
    n11 = ((v[:-1] == 1) & (v[1:] == 1)).sum()
    
    n_total = n00 + n01 + n10 + n11
    if (n00 + n01) == 0 or (n10 + n11) == 0:
        return np.nan
    
    pi_01 = n01 / (n00 + n01)
    pi_11 = n11 / (n10 + n11)
    pi_combined = (n01 + n11) / n_total
    
    if pi_01 == 0 or pi_01 == 1 or pi_11 == 0 or pi_11 == 1 or pi_combined == 0 or pi_combined == 1:
        return np.nan
    
    ll_null = (n00 + n10) * np.log(1 - pi_combined) + (n01 + n11) * np.log(pi_combined)
    ll_alt = (n00 * np.log(1 - pi_01) + n01 * np.log(pi_01) +
              n10 * np.log(1 - pi_11) + n11 * np.log(pi_11))
    lr_stat = -2 * (ll_null - ll_alt)
    
    p_value = 1 - stats.chi2.cdf(lr_stat, df=1)
    return p_value


def diebold_mariano(returns, var_a, var_b):
    aligned = pd.concat([returns, var_a, var_b], axis=1).dropna()
    aligned.columns = ["ret", "var_a", "var_b"]
    
    loss_a = (aligned["ret"] - (-aligned["var_a"])) ** 2
    loss_b = (aligned["ret"] - (-aligned["var_b"])) ** 2
    
    diff = loss_a - loss_b
    n = len(diff)
    
    mean_diff = diff.mean()
    sd_diff = diff.std()
    
    dm_stat = mean_diff / (sd_diff / np.sqrt(n))
    p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
    
    return dm_stat, p_value


def kupiec_summary(viol_dict, alpha, market, level):
    rows = []
    for method, v in viol_dict.items():
        p_val, x, n = kupiec_test(v, alpha)
        rows.append({
            "Market": market,
            "Level": level,
            "Method": method,
            "Expected": int(n * alpha),
            "Actual": x,
            "Rate %": round(x / n * 100, 2),
            "Kupiec p-val": round(p_val, 4) if not np.isnan(p_val) else "—",
            "Pass": "PASS" if p_val > 0.05 else "FAIL" if not np.isnan(p_val) else "—",
        })
    return pd.DataFrame(rows)


def christoffersen_summary(viol_dict, market, level):
    rows = []
    for method, v in viol_dict.items():
        p_val = christoffersen_test(v)
        rows.append({
            "Market": market,
            "Level": level,
            "Method": method,
            "Christ p-val": round(p_val, 4) if not np.isnan(p_val) else "—",
            "Pass": "PASS" if p_val > 0.05 else "FAIL" if not np.isnan(p_val) else "—",
        })
    return pd.DataFrame(rows)

    
    
   


