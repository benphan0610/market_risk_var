import numpy as np
import pandas as pd
from arch import arch_model

from src.config import GARCH_WARMUP, GARCH_REFIT_INTERVAL


def garch_forecasts(returns_pct, asymmetric=False):
    dates = []
    vols = []
    fitted = None
    
    for i in range(GARCH_WARMUP, len(returns_pct)):
        if (i - GARCH_WARMUP) % GARCH_REFIT_INTERVAL == 0:
            window = returns_pct.iloc[:i]
            if asymmetric:
                model = arch_model(window, vol="GARCH", p=1, o=1, q=1, dist="normal")       # GJR-GARCH(1,1)
            else:
                model = arch_model(window, vol="GARCH", p=1, q=1, dist="normal")            # Vanilla GARCH(1,1)
            fitted = model.fit(disp="off", show_warning=False)
        
        f = fitted.forecast(horizon=1, reindex=False)
        next_vol = np.sqrt(f.variance.iloc[-1, 0])
        
        dates.append(returns_pct.index[i])
        vols.append(next_vol)
    
    return pd.DataFrame({"forecast_vol": vols},
                        index=pd.DatetimeIndex(dates, name="date"))