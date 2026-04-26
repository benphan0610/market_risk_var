# Market Risk: US vs Vietnam Portfolio VaR & ES with GARCH

Project 1 of an application portfolio for the University of Toronto Rotman MFRM program (Fall 2027 intake). Maps to RSM6301H (Market Risk Management).

**Status:** Phase 1 in progress (April–June 2026).

## Objective

Construct a Value-at-Risk and Expected Shortfall framework applied side-by-side to a developed-market (US, S&P 500) and an emerging-market (Vietnam, VN-Index) equity portfolio. Compare how standard methods (Historical Simulation, Parametric Normal, GARCH(1,1) conditional) perform across markets with different volatility characteristics, tail behavior, and liquidity profiles.

## Phase 1 Scope

- US portfolio: 30-stock equal-weighted S&P 500 portfolio (2010–March 2026, daily, via yfinance)
- Vietnam portfolio: equal-weighted basket of VN-Index components (sample size pending data quality, via vnstock)
- Three VaR/ES methods on both portfolios: historical simulation, parametric normal, GARCH(1,1) conditional
- Kupiec unconditional coverage backtesting on both
- Side-by-side comparison: where do US-calibrated methods break down on Vietnam data?
- Matplotlib visualizations

## Phase 2 Expansion (planned)

Christoffersen conditional coverage, GJR-GARCH (capturing leverage effect, particularly relevant for VN), Diebold-Mariano forecast comparison, stress testing on historical crisis windows including 2018 VN drawdown and COVID 2020, Plotly dashboard, Monte Carlo VaR, Student-t parametric.

## Setup

```bash
conda create -n mfrm-market-risk python=3.13
conda activate mfrm-market-risk
pip install -r requirements.txt
```

## Repository structure

```
data/processed/   cleaned datasets (US + VN)
notebooks/        analysis notebooks (numbered execution order)
src/              modular functions
tests/            pytest unit tests
results/          figures and outputs
```

## Data Sources

- US equity: Yahoo Finance via `yfinance`
- Vietnam equity: TCBS/SSI via `vnstock` (free, public APIs)
- Risk-free rate: Treasury yields via FRED (US); SBV reference rates (VN)
- Note: vnstock data quality is inconsistent — see `data/raw/data_quality_notes.md` (TBD) for documented gaps and adjustments