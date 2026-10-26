# Viva preparation — likely questions

**Why did you take the log of the price?** Stabilises variance (price changes scale with the level) and makes first differences = percentage returns.

**What does the ADF test check? What if p > 0.05?** H0: unit root. p > 0.05 → cannot reject → non-stationary → difference the series.

**Why also KPSS?** Its null is reverse (stationary). Agreement of both tests is stronger evidence.

**How did you decide d = 1?** Log price fails ADF; its first difference passes; a second difference is unnecessary (over-differencing).

**Read ACF/PACF — how do you pick p and q?** PACF cutting off at lag p → AR(p); ACF cutting off at q → MA(q); both decaying → ARMA. Returns of gold show almost nothing significant, so p, q are small.

**AIC vs BIC?** Both penalise complexity; BIC (k·ln n) penalises more, so prefers simpler models. We chose by BIC for parsimony; AIC shown for comparison.

**Why is ARIMA no better than the naive forecast?** Gold is close to a random walk (weak-form efficient market): past prices carry little linear information about tomorrow's return. ARIMA's value is the drift and the interval.

**What is the drift term?** Average daily log change; in ARIMA(p,1,q) it is the constant in the differenced equation.

**Why SARIMA with period 5?** To test a weekly trading cycle. If seasonal strength ≈ 0 and SARIMA doesn't improve BIC/RMSE, the added parameters aren't justified.

**What is the Diebold–Mariano test?** Tests whether two forecasts have equal accuracy (squared-error loss); p > 0.05 → difference not significant.

**What is volatility clustering? What did you do about it?** Large moves follow large moves; residual ARCH-LM test rejects constant variance. GARCH(1,1) models time-varying variance → interval widens in turbulent periods.

**What does Ljung-Box test?** H0: residuals are white noise (no autocorrelation up to lag m). We want p > 0.05.

**Why one-step-ahead evaluation with `append(refit=False)`?** Mimics production: parameters fixed from training, model absorbs each new observation. Avoids look-ahead bias.

**Limitations?** Univariate; ignores USD, real yields, inflation, geopolitics; structural breaks; normal/t interval assumptions. Extension: VAR/regression with ARMA errors.

**Is this usable for trading?** No — no edge over naive demonstrated; transaction costs; educational only.
