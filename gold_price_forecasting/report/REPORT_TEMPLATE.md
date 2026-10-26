# Daily Gold Price Forecasting using ARIMA, SARIMA and GARCH
**Course:** Applied Time Series Analysis (702DB0E007) | **Team:** Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074) | **Faculty:** Prof. Kapil Rathor

## 1. Introduction
Why gold matters (safe-haven asset, inflation hedge, central-bank reserves); why forecasting is hard; objectives (below).
* Objective 1: build and compare ARIMA, SARIMA and naive forecasts of daily gold price.
* Objective 2: test the random-walk hypothesis and volatility clustering.
* Objective 3: deploy the best model as a web app.

## 2. Data  *(notebook §1, §3)*
Source: Yahoo Finance, ticker GC=F, __ to __, N = __ business days. Missing values: __ days forward-filled.

## 3. Exploratory analysis  *(§2)*
Insert `figures/01_line_plot.png`, `03_hist_qq.png`. Quote mean, std, skewness, excess kurtosis, Jarque-Bera p-value.
Discuss: upward trend, fat tails, non-normal returns.

## 4. Stationarity and transformation  *(§4, §5)*
Table: ADF/KPSS for price, log price, log return. Conclusion: d = 1. Insert `04_transformations.png`.

## 5. Seasonality  *(§6)*
Seasonal strength table, `05_decomposition.png`, ANOVA across months. Conclusion: __.

## 6. ACF/PACF and model identification  *(§7, §8)*
Insert `07_acf_pacf.png`. Significant lags: __. Ljung-Box results. Why ARIMA(p,1,q) and not a seasonal model.

## 7. Model selection  *(§9)*
AIC/BIC grid (`outputs/arima_grid_search.csv`, `08_aic_bic_heatmap.png`). Chosen: ARIMA(__) by BIC; AIC picked ARIMA(__).

## 8. Forecast evaluation  *(§10)*
Table from `outputs/model_comparison.csv` (RMSE, MAE, MAPE, directional accuracy, DM p-value). Insert `09_test_forecasts.png`.
Discussion: does any model beat naive significantly? Link to the efficient-market hypothesis.

## 9. Diagnostics and volatility  *(§11)*
`11_residual_diagnostics.png`, Ljung-Box/ARCH-LM table, GARCH(1,1) parameters, `12_garch_volatility.png`.

## 10. Deployment  *(§12, app.py)*
Screenshot of the Streamlit app; `13_final_forecast.png`; 30-day forecast table.

## 11. Conclusion, limitations, future work
Findings (3-4 bullets). Limitations: univariate, structural breaks, no exogenous drivers. Future: VAR with USD index and
10-year real yield (Unit 8), Prophet, LSTM comparison, rolling-origin cross-validation.

## 12. GenAI usage statement and references
Tools used and for what (≤ 10%). References: Hyndman & Athanasopoulos (FPP3); Brockwell & Davis; statsmodels; arch;
Engle (1982); Bollerslev (1986); Diebold & Mariano (1995).
