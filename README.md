# Value-at-Risk and Expected Shortfall: Developed vs Emerging Equity Markets

## Project Motivation

This project started from a question: do standard market-risk methods behave differently on developed and emerging market equities?

To explore this, I built two equal-weighted equity portfolios: 30 US large caps from the S&P 500 and 30 components of the India NIFTY 50 and applied six Value-at-Risk (VaR) and Expected Shortfall (ES) methods to each, covering the period from January 2010 through April 2026.


## Project Components

**Four static methods including:**
- Historical Simulation 
- Normal, 
- Student's t
- Monte Carlo 

**Two conditional VaR methods:**
- GARCH(1,1) 
- GJR-GARCH(1,1) 

**Three formal backtests:**
- Kupiec unconditional coverage 
- Christoffersen independence
- Diebold-Mariano forecast comparison

**Stress-tested across three crisis windows + a hypothetical scenario:**
- The COVID-19 crash (2020)
- The China devaluation (August 2015) 
- Volmageddon (February 2018) 
- Hypothetical −10% single-day shock


## Project Structure

The project is structured as six notebooks that run in order. Each notebook reads its input data from `data/processed/` and writes its output back to the same location, so any single notebook can be re-run independently as long as its upstream dependencies are present.

**Notebook 01 — Data and returns.** Downloads daily close prices from yfinance for both ticker lists, computes log returns, drops tickers with insufficient history, and constructs equal-weighted daily portfolios with daily rebalancing.

**Notebook 02 — Static VaR methods.** Computes Historical Simulation, Normal, Student's t, and Monte Carlo VaR/ES on a 252-day rolling window for each portfolio at the 95% and 99% confidence levels.

**Notebook 03 — Conditional VaR methods.** Fits GARCH(1,1) and GJR-GARCH(1,1) models with a 500-day initial training window and refits every 21 days. Variance forecasts are converted to VaR/ES assuming Normal innovations.

**Notebook 04 — Backtesting.** Counts violation days, runs the Kupiec unconditional coverage test and the Christoffersen independence test on each method, and applies the Diebold-Mariano test to compare selected method pairs.

**Notebook 05 — Stress testing.** Slices the VaR series into three crisis windows and computes per-window violation counts, total breach magnitude, worst single-day breach ratio, and worst observed return. Also reports a hypothetical −10% shock breach ratio against each method's most recent VaR forecast.

**Notebook 06 — Dashboard.** Combines the returns + VaR chart, backtest summary, and stress test breach ratios into a single self-contained interactive HTML file using Plotly.

All numerical work lives in `src/` modules. The notebooks import from `src/`, pass data between steps, and save artifacts. Tests for the modules are in `tests/`.


## What I found

**1. The 99% level fails for almost every method**

At the 95% level, most methods produced violation rates close to 5% and passed the Kupiec test. At the 99% level, almost every method on both markets fails Kupiec, with a lot of violations.

Normal VaR fails by the largest margin. The US Normal 99% method had 95 violations against a 2.5% rate against a designed 1%. The reason is that equity returns have fatter tails than the Normal distribution allows.

Even GARCH and GJR-GARCH fail at 99%. Both models adapt their volatility forecasts over time, but they assume Normal innovations. So even when the variance forecast is correctly elevated, the model still cannot match the size of the largest losses that actually happen.

**2. GARCH works during gradual buildups but not during sudden shocks**

During COVID 2020 on the US portfolio, GARCH and GJR-GARCH performed much better than static methods. Their worst breach ratios were 3.1 and 3.0, compared to Historical Simulation at 6.9 and Normal at 5.8. By the worst day of the crash, GARCH had been seeing rising volatility for several weeks. 

For Volmageddon 2018, it was the opposite. The S&P 500 dropped about 4% on February 5 with no warning. The day before was an ordinary trading day. With no buildup, GARCH had nothing to adapt to. Its worst breach ratio was 3.6, still better than Historical's 8.3, but not by the same margin we saw in COVID.

**3. Violations cluster in time, even for GARCH**

The Christoffersen test asks whether violations arrive independently or bunch up in time and most methods fail this test, including GARCH and GJR-GARCH at 95% on the US portfolio.

GARCH should handle clustering by design but why does it still fail? I believe there are two reasons. First, the model only refits its parameters every 21 days (I chose 21 days representing 21 trading days per month). Within each block of 21 days, the parameters are frozen and only the variance forecast updates. During regime changes this creates a lag. Second, even with a correctly elevated variance forecast, the Normal innovation assumption cannot match the kind of multi-day extreme moves that real markets occasionally produce.

**4. The same method does not behave the same on both markets**

I did multiple methods because I want to study how differ they are on different type of markets. India GARCH at 95% passed Kupiec with a 4.64% violation rate. US GARCH at 95% also passed at 5.31%. At 99%, the US Normal violation rate at 2.5% is worse than India's at 2.0%.

I also did the Diebold-Mariano test. On India, GARCH significantly beats Historical (DM = 2.47, p = 0.013). On US, the same comparison is not statistically significant (DM = -1.34, p = 0.18). A possible explanation is that India's portfolio has lower volatility and lower kurtosis than the US portfolio, so distributional assumptions misspecify the US tails more severely. Isn't that emerging market should be more volatile than developed market? I am still looking for the reason...

GJR-GARCH was expected to beat vanilla GARCH because it captures the leverage effect. On the US market, this held weakly. On India market, GJR actually underperformed GARCH significantly (DM = -3.46, p < 0.001). I believe the reason is not from the data alone but also because of the differences in the market structure and other factors.


## Assumptions

These are the assumptions and choices that I made for the project:

**Sample window: January 2010 through April 2026.**
Data starts in 2010 because yfinance coverage of NSE India is more reliable from that point onward. I intended to do stress testing on the 2008 Global Financial Crisis but the data was not reliable enough for the India market so I excluded that event.

**Equal-weighted portfolios with daily rebalancing.** 
I chose equal weights to keep portfolio construction simple and identical across markets, so any cross-market difference reflects underlying return dynamics rather than weighting choices. A market-cap weighted portfolio would be more realistic but would introduce idiosyncrasies from large-cap concentration in each index.

**30 tickers per market.** 
Both portfolios use 30 components rather than the full S&P 500 or NIFTY 50. Using all 500+ S&P names would require a survivorship-corrected database which yfinance does not provide one easily. I think 30 is enough to diversify away most idiosyncratic risk while keeping the universe small and tractable.

**252-day rolling window for static methods.** 
252 days stand for 252 trading days per year. Shorter windows like 60 or 120 days would adapt faster but will add noise. Longer windows like 1000 days would smooth out short-term noise but lag during regime changes.

**500-day initial training window for GARCH.** 
GARCH parameter estimates are noisy on small samples. 500 days should gives the model enough history to fit stable parameters before the first forecast.

**21-day refit interval for GARCH.** 
This represents roughly one trading month. Refitting daily would be ideal in principle but that would more computationally expensive over the full sample. The Christoffersen failures observed in this project may partly reflect this lag.

**Normal innovations for both GARCH and GJR-GARCH.** 
Both models assume that standardized residuals follow a Normal distribution just to keep things simple. This is the most common GARCH specification but is a poor fit for equity returns at the 99% confidence level. This choice is the main reason GARCH-based methods fail Kupiec at 99% in this project.

**Three crisis windows for stress testing: COVID 2020, China 2015, Volmageddon 2018.** 
Selected to span different types of shocks: a sustained crisis with gradual buildup (COVID), a shorter sharp regime change (China devaluation), and a single-day shock with no buildup (Volmageddon). This allows the project to test whether different methods are differentially sensitive to shock structure, not just magnitude.


## How to run

**Prerequisites**

- Python 3.10 or higher (I used Python 3.14)
- Conda (or Miniconda) for environment management

**Setup**

Clone the repository, then from the project root:

```bash
conda create -n market-risk python=3.12 -y
conda activate market-risk
pip install -r requirements.txt
```

**Run the notebooks**

The notebooks are designed to run in order. Each writes its outputs to `data/processed/` and downstream notebooks read from there.

```bash
jupyter notebook
```

Then run, in this order:

1. `notebooks/01_data_and_returns.ipynb` 
2. `notebooks/02_var_methods_static.ipynb` - This note takes a long time to load because it will have to compute various methods (est. 25-30min)
3. `notebooks/03_var_methods_garch.ipynb` 
4. `notebooks/04_backtesting.ipynb` 
5. `notebooks/05_stress_testing.ipynb`
6. `notebooks/06_dashboard.ipynb`

**Run the tests**

```bash
pytest tests/ -v
```

All tests should pass. 21 tests covering the data utilities, VaR methods, GARCH models, backtests, and stress test functions.

**View the dashboard**

After running notebook 06, open `results/var_dashboard.html` in any browser. The dashboard works offline but does require an internet connection on first load.


## Project structure
```
market_risk_var/
│
├── data/
│   ├── raw/               
│   └── processed/         # Returns, portfolios, VaR series, summaries
│
├── notebooks/
│   ├── 01_data_and_returns.ipynb
│   ├── 02_var_methods_static.ipynb
│   ├── 03_var_methods_garch.ipynb
│   ├── 04_backtesting.ipynb
│   ├── 05_stress_testing.ipynb
│   └── 06_dashboard.ipynb
│
├── src/                   # All numerical work lives here
│   ├── config.py          # Paths, tickers, parameters
│   ├── data_utils.py      # Download, returns, portfolios, CSV I/O
│   ├── var_methods.py     # Historical, Normal, Student-t, Monte Carlo
│   ├── garch_methods.py   # GARCH, GJR-GARCH walk-forward forecasts
│   ├── backtest.py        # Kupiec, Christoffersen, Diebold-Mariano
│   └── stress.py          # Crisis-window stress test metrics
│
├── tests/                 # Unit tests for each module
│   ├── test_data_utils.py
│   ├── test_var_methods.py
│   ├── test_garch_methods.py
│   ├── test_backtest.py
│   └── test_stress.py
│
├── results/
│   └── var_dashboard.html # Interactive dashboard
│
├── requirements.txt
└── README.md
```

## References

The methods implemented in this project come from the following sources:

**Backtesting:**
- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." *Journal of Derivatives*, 3(2), 73–84.
- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." *International Economic Review*, 39(4), 841–862.
- Diebold, F.X. and Mariano, R.S. (1995). "Comparing Predictive Accuracy." *Journal of Business & Economic Statistics*, 13(3), 253–263.

**Volatility models:**
- Engle, R.F. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation." *Econometrica*, 50(4), 987–1007.
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." *Journal of Econometrics*, 31(3), 307–327.
- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." *Journal of Finance*, 48(5), 1779–1801.

**Implementation libraries:**
- Sheppard, K. (2024). `arch`: Autoregressive Conditional Heteroskedasticity (ARCH) and other tools for financial econometrics, written in Python. Available at https://arch.readthedocs.io

## Author
**Benjamin Phan**
