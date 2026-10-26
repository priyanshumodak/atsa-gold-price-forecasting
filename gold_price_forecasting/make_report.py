"""Generate a concise results report without inventing findings."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent


def table(frame):
    return "```text\n" + frame.to_string(index=False) + "\n```"


def make_report():
    meta = json.loads((ROOT / "models/model_meta.json").read_text())
    scores = pd.read_csv(ROOT / "outputs/model_comparison.csv").round(4)
    stationarity = pd.read_csv(ROOT / "outputs/stationarity.csv")
    diagnostics = pd.read_csv(ROOT / "outputs/residual_diagnostics.csv").round(5)
    forecast = pd.read_csv(ROOT / "outputs/forecast_next_30_days.csv")
    text = f"""# Gold price forecasting: computed results

Course: Applied Time Series Analysis, B.Tech AI Semester VII, 2026-27.
Team members and roll numbers: Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074).

## Objective and dataset
Forecast daily COMEX gold futures closing prices in USD per troy ounce.
Source: {meta['data_source']}. Ticker: {meta['ticker']}.
Sample ends {meta['trained_until']}; {meta['n_obs']} regular business-day observations.
Missing weekdays are forward-filled from past observations. These include exchange
holidays; the generic weekday calendar is an approximation.

## Method
Line, lag-scatter, histogram and QQ plots describe prices and log returns.
ADF and KPSS assess stationarity. Logarithms and first differences form returns.
Seasonal decomposition examines periods of 5, 21 and 252 business days.
ACF/PACF motivate candidate AR/MA orders; an ARIMA grid is fitted only on
the training period. BIC selects ARIMA{tuple(meta['order'])} with drift.
Exploratory plots use the whole sample; they must not be used to tune the
candidate grid after looking at hold-out scores.

## Stationarity
{table(stationarity)}

## Evaluation
The last {meta['test_days']} business days are held out. One-step predictions
use previous observations with training parameters fixed, against a naive baseline
and a weekly SARIMA competitor. Separate fixed-origin multi-step forecasts are
plotted to show the harder deployment setting. Exponentiating log forecasts gives
conditional medians, not bias-corrected conditional price means.

{table(scores)}

The selected ARIMA RMSE is {meta['test_rmse_model']:.2f} USD versus
{meta['test_rmse_naive']:.2f} USD for the naive baseline. A lower error is better;
there is no assumption that ARIMA must outperform the baseline. The reported
loss-difference test uses a HAC standard error and is an asymptotic comparison.

## Residual checks
{table(diagnostics)}

Small Ljung-Box p-values indicate remaining serial dependence; small ARCH-LM
p-values indicate changing variance. GARCH bands are an approximate normal
quantile calculation, despite fitting Student-t innovations. Their nominal
coverage is not established by this project.

## Future forecast
{table(forecast.head(10))}

Full table: `outputs/forecast_next_30_days.csv`. Figures: `figures/`.
Run `streamlit run app.py` for an interactive forecast and CSV export.

## Limitations and discussion
The model uses only historical prices and ignores currency, rates, inflation and
news. Futures roll effects and calendar filling can affect returns. Discuss the
actual seasonal strengths, residual checks, and baseline comparison in the notebook;
do not infer market efficiency from a nonsignificant test alone.

## References and assistance disclosure
Yahoo Finance (GC=F); statsmodels ARIMA documentation; Hyndman and Athanasopoulos,
Forecasting: Principles and Practice, third edition; arch package documentation.
This implementation was prepared with AI assistance. Team members should record
their actual contributions and check the course's stated GenAI policy with faculty.
"""
    (ROOT / "report/RESULTS.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    make_report()
