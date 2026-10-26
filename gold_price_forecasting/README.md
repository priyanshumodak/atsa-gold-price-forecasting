# Gold Price Prediction Mini Project

Applied Time Series Analysis, B.Tech AI Semester VII, 2026-27.

The notebook covers all 11 steps in the supplied slide: collection; line/scatter/histogram/QQ plots and descriptive statistics; missing values; ADF/KPSS; log transformation and differencing; seasonality and decomposition; ACF/PACF; AR/MA/ARMA/ARIMA/SARIMA identification; lag selection; AIC/BIC; and Streamlit deployment. It also compares against a naive baseline and examines residuals and GARCH volatility.

## Run on Windows

From the outer project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r gold_price_forecasting\requirements.txt
.\.venv\Scripts\python.exe gold_price_forecasting\run_analysis.py
.\launch.ps1
```

If PowerShell script execution is disabled, launch directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run gold_price_forecasting\app.py
```

The app can run before training: it downloads data and fits the chosen ARIMA order. Upload a CSV in the sidebar for offline use. To inspect the notebook interactively, start Jupyter from the inner project folder. Run all cells in order.

## Real data

Yahoo Finance ticker `GC=F` is COMEX gold futures in USD per troy ounce, not Indian retail gold per gram. Data is downloaded from 2015 onward when the analysis runs. For offline analysis, provide `data/gold_daily.csv` with Date, Open, High, Low, Close, Volume columns (Date and Close are sufficient for the app). Use positive numeric prices and ISO dates. No synthetic dataset is substituted automatically. Internet failures stop the analysis unless a real cached file exists.

## Deliverables

- `gold_price_forecasting.ipynb`: editable analysis with interpretation guide.
- `gold_price_forecasting.executed.ipynb`: generated notebook with actual results.
- `figures/`: saved analysis charts.
- `outputs/`: stationarity, selection, evaluation, diagnostics and forecast CSVs.
- `models/`: fitted model and metadata.
- `report/RESULTS.md`: generated report using computed results.
- `report/REPORT_TEMPLATE.md` and `VIVA_PREP.md`: submission and presentation guidance.
- `app.py`: interactive forecast, intervals and CSV download.

## Interpretation

BIC selects an ARIMA model on training data. The final 100 business days are held out for evaluation against naive and seasonal models. One-step updated forecasts and fixed-origin multi-step forecasts answer different questions and are shown separately. The final model is refitted to all observations. Exponentiated log predictions are medians; GARCH normal-quantile bands are approximate. Business weekdays include some exchange holidays, filled with the last known price. Do not claim that ARIMA beats the baseline until the measured results support it.

Team: Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074). Interpret your actual results and include an honest assistance disclosure. The supplied course PDF describes a real-world mini project for teams of 2-3 and states a 10% GenAI limit with references; check how that applies with faculty before submission. This project was prepared with AI assistance.
