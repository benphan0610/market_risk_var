import pandas as pd

def compute_window_metrics(returns, var_series, start, end):
    aligned = pd.concat([returns, var_series], axis = 1).dropna()
    aligned.columns = ["ret", "var"]
    window = aligned.loc[pd.to_datetime(start):pd.to_datetime(end)]
    
    violations = window["ret"] < -window["var"]
    breach_days = window[violations]
    
    breach_amounts = (-breach_days["ret"]) - breach_days["var"]
    breach_ratios = (-breach_days["ret"]) / breach_days["var"]
    
    return {
        "n_violations": violations.sum(),
        "total_breach": breach_amounts.sum(),
        "worst_breach_ratio": breach_ratios.max() if len(breach_days) else 0,
        "avg_breach_severity": breach_amounts.mean() if len(breach_days) else 0,
        "worst_return": window["ret"].min(),     
    }