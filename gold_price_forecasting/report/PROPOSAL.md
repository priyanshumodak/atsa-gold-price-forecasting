# Project proposal

**Title:** Daily Gold Price Forecasting using ARIMA and SARIMA

**Course:** Applied Time Series Analysis, B.Tech AI Semester VII, 2026-27

**Team:** Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074)

**Problem:** Estimate future daily COMEX gold futures closing prices and quantify forecast uncertainty. Compare statistical models with a last-price baseline rather than assuming predictive improvement.

**Dataset:** Yahoo Finance GC=F daily OHLCV observations from January 2015 onward. Unit: USD per troy ounce. Preserve the downloaded CSV for reproducibility. These are futures prices, not Indian jewellery prices.

**Method:** Validate dates and positive prices; account for missing business weekdays; explore descriptive statistics and line/scatter/histogram/QQ plots; apply ADF/KPSS tests; compare log levels and differences; inspect seasonality, decomposition and ACF/PACF; fit an ARIMA order grid selected on training AIC/BIC; compare weekly SARIMA and naive forecasts on a chronological hold-out. Diagnose residuals and investigate GARCH volatility.

**Deliverables:** Executed notebook, dataset snapshot, charts, model-comparison and forecast CSVs, saved model, technical report and Streamlit demo.

**Success criteria:** Reproducible processing, no future observations in forecast inputs, transparent comparison with the naive baseline, interpretable uncertainty, and a working app. Better-than-baseline accuracy is an empirical question.

**Review milestones:** Dataset and EDA; transformations and model selection; hold-out evaluation and diagnostics; final report and demo. Assign actual owners and dates before the mid-term review.
