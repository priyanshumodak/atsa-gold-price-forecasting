# Gold price forecasting: computed results

Course: Applied Time Series Analysis, B.Tech AI Semester VII, 2026-27.
Team members and roll numbers: Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074).

## Objective and dataset
Forecast daily COMEX gold futures closing prices in USD per troy ounce.
Source: Yahoo Finance live (GC=F). Ticker: GC=F.
Sample ends 2026-10-26; 3082 regular business-day observations.
Missing weekdays are forward-filled from past observations. These include exchange
holidays; the generic weekday calendar is an approximation.

## Method
Line, lag-scatter, histogram and QQ plots describe prices and log returns.
ADF and KPSS assess stationarity. Logarithms and first differences form returns.
Seasonal decomposition examines periods of 5, 21 and 252 business days.
ACF/PACF motivate candidate AR/MA orders; an ARIMA grid is fitted only on
the training period. BIC selects ARIMA(0, 1, 0) with drift.
Exploratory plots use the whole sample; they must not be used to tune the
candidate grid after looking at hold-out scores.

## Stationarity
```text
          series  ADF stat  ADF p  KPSS stat  KPSS p        verdict
           Price    0.2620 0.9755     6.6929    0.01 non-stationary
       Log price    0.6940 0.9897     7.9639    0.01 non-stationary
Log return (d=1)  -14.4617 0.0000     0.2149    0.10     stationary
```

## Evaluation
The last 100 business days are held out. One-step predictions
use previous observations with training parameters fixed, against a naive baseline
and a weekly SARIMA competitor. Separate fixed-origin multi-step forecasts are
plotted to show the harder deployment setting. Exponentiating log forecasts gives
conditional medians, not bias-corrected conditional price means.

```text
               Unnamed: 0    RMSE     MAE  MAPE %  Directional acc %  DM p-value vs naive
      Naive (random walk) 60.5337 45.7090  1.0763                NaN                  NaN
     ARIMA(1, 1, 4) [AIC] 60.6684 45.5546  1.0721               53.0               0.7339
     ARIMA(0, 1, 0) [BIC] 60.6723 45.7587  1.0778               49.0               0.4639
SARIMA(0, 1, 0)x(1,0,1,5) 60.6085 45.7001  1.0763               50.0               0.7014
```

The selected ARIMA RMSE is 60.67 USD versus
60.53 USD for the naive baseline. A lower error is better;
there is no assumption that ARIMA must outperform the baseline. The reported
loss-difference test uses a HAC standard error and is an asymptotic comparison.

## Residual checks
```text
                      test  p-value                    reading
 Ljung-Box (resid), lag 10  0.08397                       pass
 Ljung-Box (resid), lag 20  0.00059 FAIL (assumption violated)
Ljung-Box (resid²), lag 10  0.00000 FAIL (assumption violated)
          ARCH-LM, 10 lags  0.00000 FAIL (assumption violated)
   Jarque-Bera (normality)  0.00000 FAIL (assumption violated)
```

Small Ljung-Box p-values indicate remaining serial dependence; small ARCH-LM
p-values indicate changing variance. GARCH bands are an approximate normal
quantile calculation, despite fitting Student-t innovations. Their nominal
coverage is not established by this project.

## Future forecast
```text
      date  forecast  arima_lo  arima_hi  garch_lo  garch_hi
2026-10-27   4039.29   3957.84   4122.41   3942.00   4138.98
2026-10-28   4040.87   3926.13   4158.97   3903.90   4182.65
2026-10-29   4042.46   3902.33   4187.62   3875.26   4216.87
2026-10-30   4044.05   3882.61   4212.19   3851.51   4246.21
2026-11-02   4045.63   3865.50   4234.16   3830.87   4272.44
2026-11-03   4047.22   3850.25   4254.28   3812.44   4296.46
2026-11-04   4048.81   3836.39   4272.99   3795.68   4318.82
2026-11-05   4050.40   3823.65   4290.61   3780.25   4339.86
2026-11-06   4051.99   3811.80   4307.32   3765.90   4359.83
2026-11-09   4053.58   3800.72   4323.28   3752.44   4378.89
```

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
