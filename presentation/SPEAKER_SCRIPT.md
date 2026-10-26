# Slide-by-slide speaker script

Priyanshu Modak (I080) | Vishesh Dokania (I019) | Parth Zanwar (I074)

## Slide 1: Gold Price Forecasting

Good morning, Professor. Our project studies daily gold futures with the complete ATSA workflow. We first build and evaluate the model in USD per troy ounce, then convert forecasts into rupees per gram for four purities. We will show measured results and limitations. The analysis snapshot ends October 26, 2026.

## Slide 2: The questions we investigated

This is a univariate time-series study with a demonstrable application. Success means correct preprocessing, a defensible evaluation and clear uncertainty. It does not require the most complex model to win. The Indian-price output estimates metal value, not a city-specific retail quote.

## Slide 3: All 11 required ATSA steps

Map the work explicitly to the supplied slide. EDA includes line plots, scatter plots, histograms, QQ plots and descriptive statistics. Residual diagnostics, baseline evaluation and optional GARCH extend the checklist. The walkthrough identifies exact notebook sections and output files for each step.

## Slide 4: Real data and provenance

Show data/gold_daily.csv and PROVENANCE.md. The actual analysis uses real historical market observations. It is not Indian retail or MCX data. A rolling futures series can contain contract-roll effects, and current-session data may be provisional. FX is a separate dataset used for display conversion.

## Slide 5: Architecture: analysis and application

The app reads the default order from metadata and refits the selected model on its selected history. It does not use the saved pickle as its main forecasting path. The notebook provides a separate saved-model helper. SARIMA comparison and GARCH are notebook analyses; the interactive app uses ARIMA. GitHub publication is verified. The user confirmed Streamlit deployment on October 27, 2026; the exact production URL was not supplied for independent verification.

## Slide 6: Cleaning and chronological split

Forward fill carries the last known price; no future price is used. Generic Monday-Friday indexing includes exchange holidays and introduces some zero returns. The hold-out consists of regularised weekdays, not strictly 100 observed trading sessions. Random splitting would mix past and future. The grid is fitted on training only.

## Slide 7: EDA: price levels and dependence

Explain the level and rolling mean from the saved chart. These descriptive statistics use the 2,971 source observations before weekday filling. Consecutive price levels can be highly correlated simply because both share a stochastic trend. That is not proof of an exploitable forecasting signal. Lag scatter plots are saved separately.

## Slide 8: EDA: distribution and heavy tails

The QQ plot compares empirical return quantiles to normal quantiles. Tail departures suggest more extreme moves than the normal reference. Volatility is descriptive historical information, not a guaranteed future estimate. Normality failure matters especially for uncertainty assumptions; it does not automatically invalidate every point forecast.

## Slide 9: Stationarity: opposite null hypotheses

ADF has a unit-root null; KPSS has a stationarity null. Small ADF and non-small KPSS support stationarity in this sample. ADF non-rejection does not prove a unit root. A printed zero is rounded, not a literally zero probability. KPSS reports tabulated bounds. Mean-process stationarity can coexist with changing conditional variance.

## Slide 10: Transformation and selected equation

Logs express proportional changes and keep inverse forecasts positive. First differences remove the integrated level. With p=q=0 this is a log random walk with drift. A mean on the price scale would require a distribution-appropriate bias correction, such as exp(mu+v/2) for Gaussian log uncertainty. The app reports the exponentiated location without that correction.

## Slide 11: Seasonality: examine rather than assume

A 252-day period approximates an annual business-day cycle rather than an exact calendar year. Classical decomposition imposes a periodic structure and uses centred calculations, so it is exploratory here. We did not evaluate every seasonal order or annual SARIMA. The actual forecasting competitor uses seasonal order (1,0,1,5).

## Slide 12: ACF/PACF and model identification

These are finite-sample heuristics, not automatic proofs. Some spikes occur by chance across many inspected lags. AR and MA terms act on the differenced log process inside ARIMA. Moving-average innovation terms are not the same as a rolling mean. The squared-return plot concerns volatility rather than just mean predictability.

## Slide 13: The recorded 25-model search

AIC is 2k minus twice log likelihood; BIC is k log n minus twice log likelihood. BIC penalises complexity more at this sample size. Negative scores are valid. The notebook keeps finite scores and does not persist a convergence flag for every candidate. Therefore do not claim 25 certified converged fits or an optimum over all possible ARIMA models.

## Slide 14: Two evaluation designs

Appending test observations with refit=False and obtaining one-step predictions updates model states with past observations while retaining training parameters. This differs from forecasting the whole test path at once. The reported RMSE comparison is one-step; do not call it 30-day-ahead RMSE. The separate fixed-origin chart addresses the harder multi-step problem.

## Slide 15: Measured performance: naive wins RMSE

State the result directly. Naive has the lowest RMSE, while AIC ARIMA has slightly lower MAE/MAPE. Different metrics can rank models differently. BIC is a prespecified simple-model choice, not the hold-out RMSE winner. A non-small p-value fails to detect a loss difference; it does not prove equality or market efficiency. MAPE is not classification accuracy.

## Slide 16: Intervals and residual diagnostics

This is a single correlated path, not independent proof of interval calibration. Residual diagnostics use the training fit with the first initialisation residual removed. It would be false to say all assumptions passed. Longer-lag correlation, squared-residual dependence and non-normality limit strong adequacy claims. The nominal 95% bands depend on model assumptions.

## Slide 17: Optional GARCH volatility extension

ARIMA models conditional mean; GARCH models changing conditional variance. Persistence near one indicates slow decay in the fitted variance process. The final band sums predicted daily variances and uses 1.96 around the ARIMA log forecast. It is not an exact Student-t interval or a jointly simulated ARIMA-GARCH system. The interactive app does not offer a GARCH engine.

## Slide 18: Final saved forecast

This is the saved October 26 analysis snapshot. A later live app can differ because of new data or the default ten-year app history versus the notebook start in 2015. It is not a contradiction. Demonstrate outputs/forecast_next_30_days.csv and explain the difference between a point median and an uncertainty interval.

## Slide 19: INR per gram and all four karats

Precious metals use a troy ounce, not the ordinary ounce. We use linked BIS fineness values: 22K=.916 rather than exactly 22/24 and 24K fine gold=.999 rather than exactly one. These are four purity scalings of one underlying forecast, not four independently trained models. Units and conversion assumptions are visible in the app.

## Slide 20: What the Indian-price display means

The displayed history is not an observed historical INR series. We would need date-aligned historical FX and future FX modelling to build that. At fixed USD gold prices a 10% rise in INR per USD scales every INR value by 10%, without changing native-model AIC/BIC. Location, premiums, taxes and making charges explain differences from a retail quote.

## Slide 21: Professor demo: deliberate actions

Predict each effect before clicking. Purity scales the output but does not invent a new price pattern. Longer horizons create additional rows and generally broader uncertainty for the selected random walk. Changing history or order triggers a model change and can be slow. Show saved results at the end, including the naive baseline and failed diagnostic tests. Do not delete data to stage an outage.

## Slide 22: All finite setting combinations

History ranges 3..15, horizon 5..60, p/q 0..5 and d 1 or 2. The compressed CSV lists all finite setting tuples. Continuous FX inputs, arbitrary upload contents, future observations and network conditions cannot be exhaustively enumerated. The scenario matrix selects useful boundary and operational cases. High-order combinations may fail or be impractical.

## Slide 23: Decision combinations and evidence

Avoid automatic test-based buttons. Examine trend specification, sample size, structural breaks and diagnostics. If AIC improves but hold-out RMSE worsens, complexity may not generalise. Repeatedly tuning to the same hold-out biases conclusions. The walkthrough includes decision tables, the complete order catalogue and professor Q&A.

## Slide 24: Code walkthrough and deployment

The root requirements file is the runtime stack; the inner file also includes notebook dependencies. File paths are anchored to app.py. The app is deployed on Streamlit Community Cloud according to the user. Temporary deployment buttons were removed after deployment. Use the actual production URL in the viva; no URL is invented here. The walkthrough maps functions to their actual behaviour.

## Slide 25: Limitations and next steps

Separate completed work from future work. Proposed improvements include storing and filtering convergence outcomes, multiple rolling origins, horizon-specific accuracy, aligned FX and an exchange-aware calendar. Prophet, LSTM, annual SARIMA and exogenous regressors are not implemented and have no results in this project.

## Slide 26: Conclusion and handover

Our contribution is a reproducible statistical workflow and an understandable application. We can demonstrate provenance, preprocessing, model selection, baseline evaluation and currency/purity arithmetic. Every team member should explain the code and actual contributions, and disclose AI assistance in line with faculty requirements.

## Slide 27: Backup: order families and trend rules

For d=1 the app uses trend t, giving drift in first differences. For d=2 it uses no deterministic trend. So d comparisons change both differencing and trend assumptions. d=0, seasonal order controls and GARCH selection are not offered in the app. The 72-order table records these rules.

## Slide 28: Backup: failure and fallback combinations

Evidence labels distinguish verified UI checks from code-reviewed or planned scenarios. Required CSV columns are Date and Close; units must be USD per troy ounce. Invalid numeric and nonpositive prices are filtered; at least 100 valid observations are needed. Dates are sorted and duplicates keep the last. Fit warnings are not always hard failures.

## Slide 29: Backup: four questions to answer precisely

Answers: MAPE is average relative error, not classification accuracy. Weak predictable structure and estimation error can make naive competitive. A new window, order, data date or FX setting changes the app output. Jewellery quotes include local/tax/product effects absent from a futures-derived metal estimate. Never turn these results into unsupported trading claims.

## Slide 30: References and assistance disclosure

Primary references are linked in the walkthrough. The course PDF states a GenAI allowance and citation expectations. The implementation and this pack used AI assistance. Do not claim unaided authorship or automatic compliance with a numerical policy limit. This is an educational project.
