# ATSA Gold Price Forecasting: Full Professor Walkthrough

Priyanshu Modak (I080) | Vishesh Dokania (I019) | Parth Zanwar (I074)

Evidence snapshot: October 26, 2026.

## 1. How to use the professor pack

Main narrative: slides 1-26, approximately 18-22 minutes, plus a five-minute demo. Slides 27-29 are backups; slide 30 gives references. For ten minutes use slides 1,2,3,4,6,9,13,15,18,19,21,25,26.

The PPTX includes speaker notes. SPEAKER_SCRIPT.md provides the full spoken script. The walkthrough explains code, results, combinations, demonstration steps and viva answers. Results are from the saved October 26, 2026 run; the live app can differ.

All 209,664 finite setting combinations are enumerated, not batch-tested. Evidence labels distinguish measured results, reviewed code paths, and planned demonstrations.

## 2. An opening you can speak

Good morning, Professor. Our ATSA mini project analyses daily gold futures through stationarity testing, decomposition, autocorrelation and ARIMA/SARIMA modelling. We use a chronological hold-out and compare against a naive benchmark. We then provide rupees-per-gram estimates for 18K, 20K, 22K and 24K gold. A simple BIC-selected random walk with drift is competitive but does not improve the naive baseline in RMSE. We report the uncertainty and residual limitations honestly.

## 3. Team and presentation handoffs

Priyanshu Modak (I080) | Vishesh Dokania (I019) | Parth Zanwar (I074)

Suggested speaking allocation: Priyanshu introduces the problem, provenance and preprocessing; Vishesh explains statistical modelling and evaluation; Parth demonstrates the app and limitations. These are suggested speaking roles, not claims about who wrote the code. Replace with actual contributions.

Implementation and these materials used AI assistance. Explain every component and disclose actual contributions; do not assume this pack automatically meets the course PDF's stated GenAI policy.

## 4. Mapping every required ATSA step

| Step | Requirement | Evidence |
| --- | --- | --- |
| 1 | Collection | Notebook section 1; data/gold_daily.csv and PROVENANCE.md |
| 2 | EDA | Notebook section 2; line/scatter/histogram/QQ; figures 01-03 |
| 3 | Missing values | Notebook section 3; 111 weekdays forward-filled |
| 4 | Stationarity / ADF | Notebook section 4; stationarity.csv and KPSS |
| 5 | Transformations | Notebook section 5; logs and difference; figure 04 |
| 6 | Seasonality | Notebook section 6; strengths; figures 05-06 |
| 7 | ACF / PACF | Notebook section 7; figure 07 |
| 8 | Family identification | Notebook section 8; AR/MA/ARMA/ARIMA/SARIMA |
| 9 | Lags | Notebook section 9; p/q grid |
| 10 | AIC / BIC | arima_grid_search.csv and figure 08 |
| 11 | Deployment | streamlit_app.py, inner app.py, GitHub, cloud form |

## 5. Dataset: what it is and what it is not

Source is Yahoo Finance GC=F, a rolling COMEX gold futures series. The snapshot has 2,971 observations from January 2, 2015 to October 26, 2026, with OHLCV fields. Close is the target and its native unit is USD per troy ounce.

It is not Indian city-specific retail, MCX or jewellery-shop data. Contract-roll effects can affect a futures series and a current-session value may be provisional. The actual analysis uses real observations; simulated test fixtures were used only in separate app checks.

FX source is INR=X. The saved rate is 95.175003 INR per USD dated 2026-10-26. It is a dated observation, not a permanently valid current rate.

Raw-source mean is 1,966.45857 USD/oz, standard deviation 956.72956, minimum 1,050.80005 and maximum 5,318.39990. Source log-return excess kurtosis is 7.7843 and annualised volatility about 16.8%. These statistics precede weekday filling.

## 6. Preprocessing, missing dates and leakage

Notebook processing sorts dates, retains the last duplicate, converts Close to numeric, replaces invalid or nonpositive prices, reindexes to B frequency, forward-fills and drops leading missing values. It adds 111 missing weekdays (3.60%), yielding 3,082 observations.

Forward fill uses past information. Backward fill and two-sided interpolation can inject future observations. Generic weekdays include exchange holidays and introduce zero returns; this is an approximation to disclose, not an exact trading calendar.

App uploads require Date and Close, parseable dates, positive numeric prices and at least 100 valid source observations. The app sorts and deduplicates. Uploaded values must be fine-gold USD per troy ounce; semantic units cannot be inferred from a numeric column.

Training is 2,982 regular observations through June 8, 2026; the hold-out is 100 regular weekdays from June 9 to October 26. Candidate fitting uses training only. Full-sample exploratory plots must not become a reason to repeatedly tune against future observations.

## 7. Explain every EDA plot

| Output | Explanation | Caution |
| --- | --- | --- |
| Line plot | Changing level and rolling mean | A trend is not proof of usable predictive information |
| Lag scatter | Price(t) versus Price(t-1), then returns | Integrated levels can look highly dependent |
| Histogram | Distribution, skewness and tails | Price and return distributions differ |
| QQ plot | Empirical versus normal quantiles | Tail departures limit Gaussian assumptions |
| Descriptive statistics | Counts, moments and volatility | State whether raw or regularised observations are used |

## 8. Stationarity and all ADF/KPSS outcomes

Weak stationarity concerns a stable mean and variance with autocovariance depending on lag. Mean-process stationarity does not imply constant conditional variance at every date.

ADF null is a unit root; KPSS null is level stationarity (regression c here). ADF uses AIC-based lag selection; KPSS uses automatic lag selection. The 5% threshold is an aid, not proof.

| ADF | KPSS | Interpretation |
| --- | --- | --- |
| Reject | Do not reject | Stationarity supported for the tested series |
| Do not reject | Reject | Non-stationarity evidence; investigate transformation/differencing |
| Reject | Reject | Conflicting; inspect trend, breaks and test specifications |
| Do not reject | Do not reject | Inconclusive; limited power may matter |

## 9. Actual stationarity evidence

Price: ADF p=.9755, KPSS p at lower reported bound .01. Log price: ADF p=.9897, KPSS lower bound .01. Log return: ADF about 6.83e-27, KPSS upper reported bound .10. The saved CSV rounds a very small ADF p to zero; it is not literally a zero probability.

These results support first-differenced logs for the mean process in this sample. ADF failure to reject does not prove a unit root. KPSS tabulated bounds are not exact tail probabilities. A second-difference stationarity result would not prove first differences were insufficient.

## 10. Transformation and ARIMA mathematics

z_t = log(P_t); r_t = z_t - z_(t-1). Logs express proportional changes and preserve positive inverse forecasts. First differencing addresses the integrated level; it does not guarantee Gaussian or homoskedastic errors.

ARIMA(p,d,q) differences its target d times and models the result using p autoregressive and q moving-average innovation terms. The target supplied here is log price. SARIMA adds seasonal (P,D,Q,s).

Selected ARIMA(0,1,0) with drift: z_t = z_(t-1) + c + e_t. Its h-step log location is z_T + h*c. The app reports exp(mu_h), a conditional median under the log model. A Gaussian conditional price mean would require exp(mu_h + v_h/2), which is not the default.

The app sets trend t for d=1, producing drift after differencing. For d=2 it uses trend n, so a d=2 comparison changes deterministic terms as well. App d=0 is not available.

## 11. Seasonality and decomposition

Classical additive decomposition of log price examines periods 5, 21 and 252 business days. Recorded strengths are .0002, .0084 and .1747. Weekly/monthly strengths are weak; annual descriptive strength is more noticeable.

A 252-business-day annual approximation is not exact calendar seasonality. Decomposition imposes a periodic structure and uses centred operations. It is exploratory here, not a future-aware predictor. The monthly-return ANOVA is another descriptive check.

Only the weekly SARIMA competitor with seasonal order (1,0,1,5) is forecast and evaluated. Annual SARIMA and all seasonal permutations were not searched.

## 12. ACF/PACF: all model-family cases

| Family | Heuristic | Meaning |
| --- | --- | --- |
| AR(p) | PACF cutoff; ACF decay | AR terms model past values of a stationary/differenced process |
| MA(q) | ACF cutoff; PACF decay | Past innovations; not a rolling average |
| ARMA | Both generally decay | AR and MA in stationary differences |
| ARIMA | Differencing plus ARMA | Our main family; logs supplied as target |
| SARIMA | Additional seasonal dynamics | Weekly competitor only |
| GARCH | Squared-return dependence / ARCH | Conditional variance rather than mean trend |

## 13. Model selection and all 25 actual candidates

The notebook tries all p and q in {0,1,2,3,4}, d fixed at 1: exactly 25 tuples, each with drift and the same training target. ACTUAL_25_ARIMA_RESULTS.csv contains the recorded scores, sorted by BIC.

Minimum AIC is ARIMA(1,1,4), approximately -18852.29. Minimum BIC is ARIMA(0,1,0), approximately -18836.86. AIC=2k-2 log L and BIC=k log n-2 log L. Compare scores only on comparable likelihood/data settings. Negative scores are valid.

Convergence warnings occurred in the executed notebook. The grid retains finite scores without persisting/filtering every convergence flag. Therefore the recorded ranking is not a claim that every candidate converged or a global optimum over all possible orders.

## 14. Evaluation designs and information availability

One-step evaluation fits training parameters and updates the state using previous hold-out observations with refit=False. Each prediction conditions on the past, not its own actual target. Appending observations and asking for one-step predictions is distinct from forecasting the whole future block.

Fixed-origin evaluation forecasts all 100 dates from the training endpoint without incorporating hold-out actuals. The separate chart shows that harder problem. Reported comparison RMSE is one-step, not a 30-day fixed-origin performance estimate.

After evaluation the selected order is refitted on the full series for final outputs. Exploratory analysis uses the full sample; repeatedly changing choices after looking at plots or test scores would bias the hold-out. A prespecified grid and multiple rolling origins would strengthen the study.

## 15. Metrics and recorded results

RMSE=sqrt(mean(error^2)); MAE=mean(abs(error)); MAPE=100*mean(abs(error)/actual). RMSE emphasises large misses. Gold prices are positive, so the usual zero-denominator MAPE issue is limited here. MAPE is not classification accuracy.

Directional accuracy compares the signs of actual and predicted changes. The code excludes zero predicted directions; naive predicts no change so its directional score is undefined.

| Model | RMSE USD/oz | MAE USD/oz | MAPE % | Direction % |
| --- | --- | --- | --- | --- |
| Naive (random walk) | 60.5337 | 45.7090 | 1.0763 | Undefined |
| ARIMA(1, 1, 4) [AIC] | 60.6684 | 45.5546 | 1.0721 | 53.0 |
| ARIMA(0, 1, 0) [BIC] | 60.6723 | 45.7587 | 1.0778 | 49.0 |
| SARIMA(0, 1, 0)x(1,0,1,5) | 60.6085 | 45.7001 | 1.0763 | 50.0 |

## 16. Significance and conclusions to defend

Naive has the lowest RMSE (60.5337 versus BIC ARIMA 60.6723), while AIC ARIMA has slightly lower MAE and MAPE than the other methods. Metric rankings can differ. BIC selection is prespecified simplicity, not a test-RMSE win.

The loss-difference comparison regresses squared-error differences on a constant with a HAC standard error. BIC ARIMA versus naive p=.46395; AIC ARIMA p=.73392; SARIMA p=.70141. It is asymptotic and does not prove equality, market efficiency or universal forecasting quality.

Do not say 1.0778% MAPE equals 98.9222% accuracy. Do not say ARIMA significantly beats naive. If operational selection were solely the observed hold-out RMSE, naive would be preferred in this comparison.

## 17. Residual tests and all mean/variance cases

Training-fit residuals drop the first diffuse-initialisation residual. Ljung-Box tests serial dependence; ARCH-LM tests time-varying variance; Jarque-Bera tests normality.

Actual p-values: Ljung-Box residual lag 10 .083968; lag 20 .0005889; squared residual lag 10 4.40e-71; ARCH-LM 6.28e-45; normality effectively underflows to zero. It is incorrect to say the residuals are fully white noise or all assumptions pass.

| Mean diagnostic | Variance diagnostic | Response |
| --- | --- | --- |
| No residual correlation | No ARCH evidence | Mean/variance checks appear adequate; validate coverage too |
| Residual correlation | No ARCH evidence | Revisit mean dynamics/lags/omissions |
| No residual correlation | ARCH evidence | Investigate conditional variance |
| Residual correlation | ARCH evidence | Both mean and variance need investigation |

## 18. Intervals and optional GARCH

Fixed-origin nominal 95% ARIMA bands contain 94/100 hold-out observations. This is a single correlated path, not proof of calibrated repeated coverage at each horizon. Marginal intervals are not simultaneous guarantees for the whole future path.

Training GARCH(1,1), fitted to percentage log returns with Student-t errors, has rounded omega .0092385, alpha .0359, beta .9583 and persistence .9942. Persistence near one indicates slowly decaying fitted variance shocks.

The final GARCH band uses predicted daily variances, cumulative standard deviation and 1.96 around an ARIMA log forecast. It is approximate, not exact Student-t inference or a jointly estimated ARIMA-GARCH path simulation. Its coverage is not established. The current app shows ARIMA intervals only.

## 19. Rupees, grams and every karat

INR/g = USD/oz x INR per USD / 31.1034768 x fineness. Use a troy ounce rather than the ordinary ounce. Implemented fineness values are 18K .750, 20K .833, 22K .916 and 24K fine gold .999.

All four purity views scale one underlying gold model. The same positive factor must scale the median, history and both bounds. 22K=.916 is not exactly 22/24; 24K=.999 is the fine-gold convention explicitly used in the app.

Illustration only: the table assumes USD 4,000/oz and FX 100 INR/USD; these are teaching inputs, not current quotations.

| Karat | Fineness | Illustrative INR/g |
| --- | --- | --- |
| 18K | 0.75 | 9,645.22 |
| 20K | 0.833 | 10,712.63 |
| 22K | 0.916 | 11,780.03 |
| 24K | 0.999 | 12,847.44 |

## 20. Every FX path and price interpretation

Live INR=X is tried first; a valid rate and date are displayed. If it fails, the saved JSON supplies 95.175003 INR/USD dated 2026-10-26. If both fail, the app requires a positive manual rate. A manual override replaces conversion only; it does not forecast FX.

Selected FX is held constant across all historical and future displayed dates. History therefore revalues old USD prices at the selected rate; it is not a historically aligned INR series. A 10% FX increase scales every INR value by 10% while leaving native ARIMA fitting and AIC/BIC unchanged.

Displayed metal values exclude GST, duties, making charges, local premiums and city-specific effects. Future exchange-rate uncertainty is not included in the bands. A jewellery-shop quote is not a directly comparable evaluation target.

## 21. Every app control

| Control | Range | Effect |
| --- | --- | --- |
| Purity | 18K/20K/22K/24K | Scales display, not independent training |
| History | 3..15 years | Changes sample; live/calendar and cached/252 approximations differ |
| Horizon | 5..60 weekdays | Changes count of forecast dates, not calendar days |
| p | 0..5 | AR order after differencing |
| d | 1 or 2 | Difference order; trend t vs n |
| q | 0..5 | MA innovation order |
| FX | Positive automatic/manual | Changes display-unit conversion |
| CSV | Date/Close in USD per troy ounce | At least 100 valid prices; years slider does not trim uploads |

## 22. All permutations: what can be exhaustive

Finite combinations: 4 purities x 13 history lengths x 56 horizons x (6 p-values x 2 d-values x 6 q-values) = 209,664. ALL_209664_APP_COMBINATIONS.csv.gz lists each tuple once, labelled ENUMERATED_NOT_BATCH_TESTED.

ALL_72_MODEL_ORDERS.csv lists every app order, its trend rule and notebook-grid inclusion. ACTUAL_25_ARIMA_RESULTS.csv is the measured grid. Enumeration does not prove convergence, successful fitting, accuracy or deployment of each combination.

Arbitrary positive FX values, arbitrary CSV contents, future data, calendar edge cases and network conditions have no useful finite exhaustive catalogue. The 26-case scenario matrix selects meaningful paths and labels evidence.

## 23. A five-minute professor demo

1. Run .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py. Open http://localhost:8501. State the gold source/date and FX source/date.

2. Begin 24K, 10 years, 30 weekdays, (0,1,0). Explain last close, median, interval, AIC/BIC and the futures-derived estimate qualification.

3. Switch to 22K, 20K and 18K. Predict the price ordering first; show the comparison table. Explain that returns/pattern shape do not change under fixed positive scaling.

4. Compare horizons 5 and 60. Check row count and uncertainty. Generally increasing width is expected for the selected random walk; do not promise strict monotonic width for every arbitrary order.

5. Set manual FX to 100; demonstrate proportional change. Restore automatic FX. Native-model fit scores are not rupee-denominated accuracy scores.

6. Try (1,1,0), explain AR in returns, then optionally (0,1,1). Return to (0,1,0). Avoid slow high-order stress cases in the main demo.

7. Download selected-purity and all-purity CSVs. Show explicit units/karat/FX. If uploading, prepare a valid USD/oz file; do not upload INR/g data.

8. Open model_comparison.csv and the residual diagnostics. Close with the naive RMSE advantage and remaining assumptions. Do not hide these results.

9. Show the public GitHub source and open your actual deployed Streamlit URL. Deployment was confirmed by the user on October 27, 2026; temporary deployment buttons have been removed.

## 24. Edge cases and evidence discipline

DEMO_AND_EDGE_CASE_MATRIX.csv contains 26 paths. Previously verified runtime checks include all four purities, manual FX arithmetic, ordered bounds, a mocked real-data fallback and an earlier d=2 smoke test. Other rows are labelled code review or demo plan rather than executed checks.

Bad required columns or dates show an error. Invalid numeric/nonpositive values are removed; insufficient remaining prices stop the fit. High-order fits may warn, fail or run slowly. Warnings do not always prevent an output.

Do not delete real files to create a viva outage. Cache corruption and empty metadata are not fully hardened production paths. A numeric INR/g upload cannot be automatically recognised as wrong units.

## 25. File-by-file and function-by-function walkthrough

| File/block | Operation | Explain |
| --- | --- | --- |
| streamlit_app.py | runpy executes inner app | Root cloud entry point |
| app.py constants | Troy grams and FINENESS | Defines conversion semantics |
| load_exchange_rate | Live INR=X, then JSON | Returns positive FX, date and source |
| load_prices | Live GC=F, then real CSV | No automatic fabricated prices |
| fit_forecast | log/B-frequency/ffill/ARIMA | Caches median and bounds |
| sidebar and upload | Purity/FX/history/horizon/order | User sensitivity and validated input |
| conversion and chart | Positive factor on all series | Current-FX revaluation |
| exports and comparison | One or all purities | CSV units, karat and FX metadata |
| notebook sections 1-9 | Collection to selection | EDA/tests and training grid |
| notebook sections 10-11 | Evaluation and diagnostics | One-step, fixed-origin, GARCH |
| notebook section 12 | Refit/save/helper | Pickle helper is separate from app refit |
| run_analysis.py | NotebookClient, then report | Creates executed notebook |
| make_report.py | Reads CSVs/metadata | Generates RESULTS.md |
| requirements files | Root runtime, inner analysis | Pinned runtime; notebook stack separate |

## 26. Architecture questions to answer

Why not use the saved pickle in every app request? The app permits new history and order choices, so it refits; metadata chooses defaults. The notebook includes a separate persistence helper.

Does changing order run the grid? No, it fits the selected order. The archived notebook RMSE appears only for matching default ticker/order and is labelled archived. Changing history can still make the new fit different.

Why can live and cached histories differ? Live requests use calendar-year periods; cached slices use years*252 observations. Uploads use supplied history without applying the years slider. These are current implementation limitations.

What hosting is verified? GitHub is public and local health was checked. The user confirmed Streamlit deployment on October 27, 2026. The exact production URL has not been supplied or independently checked.

## 27. Prioritised improvements

First record convergence flags and exclude failed candidates. Next prespecify rolling-origin tests over multiple horizons, periods and data regimes. Then align historical FX and consider an INR target or joint FX scenarios.

Use an exchange-aware calendar, evaluate horizon-specific interval coverage and consider heavy-tail simulations. Add exogenous factors only with proper time-aligned information availability.

Improve upload/history consistency, archived-metric comparability and versioned data/model provenance. Annual SARIMA, Prophet, LSTM and external drivers are future work, not implemented results.

## 28. Viva: 42 questions and precise answers

1. Why choose gold?
Answer: It is a real positive financial series with changing levels, dependence and volatility, suitable for the full ATSA workflow.

2. Is the data real?
Answer: Yes. The GC=F snapshot has 2,971 historical Yahoo observations. Simulated data was used only in separate UI checks, not the reported analysis.

3. Why 3,082 rows after cleaning?
Answer: Reindexing creates 111 missing weekdays, filled from past prices. These are not 111 extra real trading observations.

4. Why use Close?
Answer: The defined target is the daily closing price. OHLCV fields are available but are not external regressors.

5. Why chronological splitting?
Answer: A random split can train on future information relative to a target; chronology matches forecasting information availability.

6. Why log prices?
Answer: Logs express proportional changes and give positive inverse forecasts. They do not guarantee stationarity or normality.

7. What is d?
Answer: The number of differences applied to log prices. The selected model uses one.

8. What is p?
Answer: The autoregressive lag order in the differenced log process.

9. What is q?
Answer: The number of lagged innovation terms. It is not a rolling-average window.

10. Why ADF plus KPSS?
Answer: Opposite null hypotheses provide a useful cross-check, although neither is definitive.

11. Does ADF p>.05 prove a unit root?
Answer: No; it fails to reject under that specification and sample, with power and structural-break limitations.

12. Does p=0 mean certainty?
Answer: No. It is rounded/underflowed. The saved log-return ADF summary is about 6.83e-27.

13. Can stationary returns have volatility clustering?
Answer: Yes. Mean-process stationarity testing and time-varying conditional variance address different questions.

14. Why p and q only through four in the notebook?
Answer: It is a tractable bounded design motivated by short-lag dynamics, not proof that no higher order can help.

15. Did all candidates converge?
Answer: Not established. Warnings occurred and per-order convergence flags were not persisted. Scores need that caveat.

16. Why does BIC favour simplicity?
Answer: Its complexity penalty is k log n; at this sample size small likelihood gains may not offset additional parameters.

17. Can AIC/BIC be negative?
Answer: Yes. Compare relative values from comparable likelihoods and datasets.

18. Why not repeatedly tune on test RMSE?
Answer: That makes the test set part of model selection and biases its evaluation. Use a validation/rolling-origin design.

19. What is ARIMA(0,1,0) with drift?
Answer: A random walk plus constant expected log change, with innovations; not a deterministic trading rule.

20. Why test SARIMA when seasonality is weak?
Answer: It supplies a concrete weekly competitor rather than assuming seasonal terms must help.

21. Was annual SARIMA tested?
Answer: No. Annual decomposition was descriptive; the evaluated seasonal competitor is (1,0,1,5).

22. Did ARIMA beat naive?
Answer: Not by RMSE. Naive is 60.5337 versus BIC ARIMA 60.6723 USD/oz on the recorded one-step hold-out.

23. Is MAPE equivalent to accuracy?
Answer: No. It is average relative regression error, not the probability of a correct classification.

24. Is direction prediction reliable?
Answer: The BIC model has 49% directional agreement in this hold-out, so useful directional advantage is not demonstrated.

25. What does the HAC comparison show?
Answer: At p about .464 for BIC ARIMA, it does not detect a squared-loss difference. It does not prove equality or efficiency.

26. Does a 95% band cover the whole future path with 95% probability?
Answer: No. Marginal forecast intervals and simultaneous path coverage are different.

27. Was interval coverage measured?
Answer: 94 of 100 fixed-origin actual values lie within ARIMA bands. One correlated path does not establish general calibration.

28. Why GARCH?
Answer: Squared-residual dependence and ARCH rejection indicate changing conditional variance. GARCH models variance, not the price trend.

29. Are the final GARCH bands exact Student-t intervals?
Answer: No. Student-t innovations were fitted but the final calculation uses normal quantiles and cumulative variance.

30. Did all residual assumptions pass?
Answer: No. Lag-20 Ljung-Box, ARCH and normality reject, limiting adequacy claims.

31. Why INR per gram?
Answer: It is familiar to Indian users; conversion is separate from the native USD/oz statistical fitting.

32. Why divide by 31.1034768?
Answer: That is grams per troy ounce. Precious metals use troy rather than ordinary ounces.

33. Why .916 rather than exactly 22/24?
Answer: The app explicitly adopts the BIS-linked 916 fineness grade.

34. Is 24K exactly pure in this implementation?
Answer: No. It is fine gold 999, or 99.9%, as stated in the interface.

35. Are there four independently trained purity models?
Answer: No. A single underlying forecast is scaled by fineness.

36. Is future USD-INR predicted?
Answer: No. A selected dated or manual rate is fixed over forecast dates and FX uncertainty is excluded.

37. Why does the value differ from the jeweller?
Answer: It is a converted futures metal value; tax, local premiums, duties and making charges are excluded.

38. Why does the app differ from the notebook?
Answer: History length, order, new observations and FX may differ. Notebook metrics are archived and labelled.

39. What happens offline?
Answer: Default paths use the real cached gold CSV and dated FX snapshot. Missing sources lead to required manual FX or an error, not fabricated observations.

40. How many combinations were evaluated?
Answer: The notebook records 25 nonseasonal candidate scores and the stated forecast competitors. The 209,664 app tuples are enumerated, not benchmarked.

41. What improvement comes first?
Answer: Persist convergence flags, strengthen rolling-origin evaluation, then align FX/calendar handling and validate intervals.

42. Who wrote the project?
Answer: State actual team contributions and AI assistance. Do not invent individual coding roles or claim numerical policy compliance without checking.

## 29. Claims to avoid

Avoid 99% accuracy. Say: BIC ARIMA MAPE was 1.0778% on the specified one-step hold-out.

Avoid ARIMA beats naive. Say: naive wins RMSE; AIC ARIMA has slightly lower MAE/MAPE.

Avoid all assumptions pass. Say: longer-lag dependence, ARCH effects and non-normality remain.

Avoid four trained karat models. Say: one gold forecast, four fineness scalings.

Avoid exact Indian retail price. Say: futures-derived INR/g metal-value estimate excluding retail charges.

Avoid every combination tested. Say: finite settings enumerated; actual score and check evidence labelled.

Avoid inventing a production URL. Say: the user confirmed Streamlit deployment; show the actual live address from your account.

## 30. Reproducibility and useful commands

Local app: .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py

Analysis: .\.venv\Scripts\python.exe gold_price_forecasting\run_analysis.py

Rebuild pack: .\.venv\Scripts\python.exe scripts\build_professor_pack.py

Pack-builder libraries: python-pptx, python-docx, reportlab plus the project dependencies. Preserve the dated CSV, metadata, charts and executed notebook for an unchanged viva; downloading again may change results.

## 31. Primary references and disclosure

Yahoo gold data: https://finance.yahoo.com/quote/GC=F/history/ ; FX: https://finance.yahoo.com/quote/INR=X/history/

statsmodels ARIMA: https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html ; time-series API: https://www.statsmodels.org/stable/tsa.html

Hyndman and Athanasopoulos, Forecasting: Principles and Practice (third edition): https://otexts.com/fpp3/

arch forecasting: https://arch.readthedocs.io/en/stable/univariate/forecasting.html

BIS fineness listing: https://lims.bis.gov.in/home/search_is_number/?is_number__doc_no=1417

NIST conversion: https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8

Streamlit: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

Implementation, documentation and this pack used AI assistance. Team members should understand and verify the work and discuss the course PDF's stated GenAI policy with faculty. This pack makes no unsupported compliance claim.
