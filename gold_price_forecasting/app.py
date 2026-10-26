"""Streamlit app — Daily Gold Price Forecaster (Step 11: Deploy the model).

Run:  streamlit run app.py
Fits an ARIMA(p,1,q)+drift on live gold data and shows a forecast with a 95% interval.
Default order is read from models/model_meta.json (written by the notebook).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Gold Price Forecaster - INR per gram", page_icon="🪙", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
META_PATH = BASE_DIR / "models/model_meta.json"
CSV_PATH = BASE_DIR / "data/gold_daily.csv"
meta = json.loads(META_PATH.read_text()) if META_PATH.exists() else {}
GRAMS_PER_TROY_OUNCE = 31.1034768
FINENESS = {"18K": 0.750, "20K": 0.833, "22K": 0.916, "24K": 0.999}


@st.cache_data(ttl=3600, show_spinner="Loading USD-INR exchange rate...")
def load_exchange_rate():
    try:
        import yfinance as yf
        yf.set_tz_cache_location(str(BASE_DIR / "data/.yf_cache"))
        frame = yf.download("INR=X", period="1mo", auto_adjust=False, progress=False, timeout=10)
        if isinstance(frame.columns, pd.MultiIndex):
            frame.columns = frame.columns.get_level_values(0)
        rates = pd.to_numeric(frame["Close"], errors="coerce").dropna()
        rates = rates[np.isfinite(rates) & (rates > 0)]
        if len(rates):
            return float(rates.iloc[-1]), str(rates.index[-1].date()), "Yahoo Finance INR=X"
    except Exception:
        pass
    cache = BASE_DIR / "data/usd_inr.json"
    if cache.exists():
        saved = json.loads(cache.read_text())
        rate = float(saved["rate"])
        if np.isfinite(rate) and rate > 0:
            return rate, saved["date"], "Saved exchange-rate snapshot"
    return None, None, None


@st.cache_data(ttl=3600, show_spinner="Downloading gold prices…")
def load_prices(ticker: str, years: int):
    try:
        import yfinance as yf
        yf.set_tz_cache_location(str(BASE_DIR / "data/.yf_cache"))
        df = yf.download(ticker, period=f"{years}y", auto_adjust=False, progress=False, timeout=20)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        s = df["Close"].dropna()
        if len(s) > 250:
            return s, f"Yahoo Finance (live, {ticker})"
    except Exception:
        pass
    if CSV_PATH.exists():
        s = pd.read_csv(CSV_PATH, index_col=0, parse_dates=True)["Close"].dropna()
        if ticker == meta.get("ticker", "GC=F"):
            return s.iloc[-int(years * 252):], f"cached file ({ticker})"
    return None, None


@st.cache_data(show_spinner="Fitting ARIMA…")
def fit_forecast(prices: pd.Series, order: tuple, horizon: int):
    y = np.log(prices.asfreq("B").ffill())
    res = ARIMA(y, order=order, trend="t" if order[1] == 1 else "n").fit()
    fc = res.get_forecast(horizon)
    ci = fc.conf_int(alpha=0.05)
    out = pd.DataFrame({
        "forecast": np.exp(fc.predicted_mean.values),
        "lower_95": np.exp(ci.iloc[:, 0].values),
        "upper_95": np.exp(ci.iloc[:, 1].values),
    }, index=fc.predicted_mean.index)
    out.index.name = "date"
    return np.exp(y), out, float(res.aic), float(res.bic)


# ---------------------------------------------------------------- sidebar
st.sidebar.link_button("Deploy to Streamlit", "https://share.streamlit.io/deploy?repository=priyanshumodak%2Fatsa-gold-price-forecasting&branch=main&mainModule=streamlit_app.py", help="Open the deployment form for this GitHub project. Sign in with GitHub if prompted.")
st.sidebar.header("Settings")
ticker = "GC=F"
karat = st.sidebar.selectbox("Gold purity", list(FINENESS), index=3)
rate, rate_date, rate_source = load_exchange_rate()
manual_fx = st.sidebar.checkbox("Set USD-INR rate manually", value=rate is None)
if manual_fx:
    rate = st.sidebar.number_input("INR for 1 USD", min_value=0.01, value=float(rate) if rate else None, step=0.10)
    rate_source, rate_date = "Manual exchange rate", "user supplied"
if rate is None:
    st.info("Enter the INR value of 1 USD in the sidebar to continue.")
    st.stop()
st.sidebar.caption(f"1 USD = ₹{rate:.4f} | {rate_date} | {rate_source}")
st.sidebar.caption("Purity: 18K 750, 20K 833, 22K 916, 24K fine gold 999.")
years = st.sidebar.slider("History (years)", 3, 15, 10)
horizon = st.sidebar.slider("Forecast horizon (business days)", 5, 60, 30)
d_p, d_d, d_q = meta.get("order", [0, 1, 0])
c1, c2, c3 = st.sidebar.columns(3)
p = c1.number_input("p", 0, 5, int(d_p))
d = c2.number_input("d", 1, 2, int(d_d))
q = c3.number_input("q", 0, 5, int(d_q))
st.sidebar.caption("All displayed prices are INR per gram. Forecast dates use weekdays and may include exchange holidays.")
st.sidebar.caption("Order defaults to the model chosen by BIC in the notebook.")

# ---------------------------------------------------------------- main
st.title("🪙 Gold Price Forecaster - ₹ per gram")
st.caption("ATSA mini project | 18K, 20K, 22K and 24K gold | Indian rupees per gram")
st.info("Estimated gold metal value from COMEX futures. Excludes GST, import duties, making charges and local premiums; jeweller prices will differ.")

uploaded = st.sidebar.file_uploader("Or upload gold price CSV", type=["csv"], help="Columns: Date, Close. Close must be fine-gold USD per troy ounce, with at least 100 observations.")
if uploaded is not None:
    try:
        frame = pd.read_csv(uploaded)
        if not {"Date", "Close"}.issubset(frame.columns):
            raise ValueError("CSV must contain Date and Close columns.")
        frame["Date"] = pd.to_datetime(frame["Date"], errors="raise", utc=True).dt.tz_convert(None).dt.normalize()
        prices = frame.set_index("Date")["Close"]
        source = f"Uploaded CSV: {uploaded.name} (verify currency and instrument)"
    except Exception as exc:
        st.error(f"Invalid CSV: {exc}")
        st.stop()
else:
    prices, source = load_prices(ticker, years)
if prices is None:
    st.error("Could not download data and no cached data/gold_daily.csv found. Check your internet connection.")
    st.stop()

try:
    prices = pd.to_numeric(prices, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    prices = prices[prices > 0].sort_index()
    prices = prices[~prices.index.duplicated(keep="last")]
    if len(prices) < 100:
        raise ValueError("At least 100 valid positive closing prices are required.")
    hist, fc, aic, bic = fit_forecast(prices, (int(p), int(d), int(q)), horizon)
except Exception as exc:
    st.error(f"Could not fit this model: {exc}")
    st.stop()
# Convert model output, every confidence bound, and history with the same FX assumption.
# Historical chart is revalued at the selected FX rate, not a historical INR backtest.
usd_last = float(hist.iloc[-1])
usd_fc = fc.copy()
conversion = float(rate) * FINENESS[karat] / GRAMS_PER_TROY_OUNCE
hist = hist * conversion
fc = fc * conversion
st.subheader(f"{karat} gold - INR per gram")
st.caption(f"Using USD-INR {rate:.4f} ({rate_date}). The selected exchange rate is held constant across history and future forecasts; FX uncertainty is excluded.")
last = float(hist.iloc[-1])
end = float(fc["forecast"].iloc[-1])

m1, m2, m3, m4 = st.columns(4)
m1.metric(f"Last close ({karat}, ₹/g)", f"₹{last:,.2f}", help=f"as of {hist.index[-1].date()}")
m2.metric(f"Forecast in {horizon} days (₹/g)", f"₹{end:,.2f}", f"{(end / last - 1) * 100:+.2f}%")
m3.metric("95% interval at horizon (INR/g)", f"₹{fc['lower_95'].iloc[-1]:,.2f} - ₹{fc['upper_95'].iloc[-1]:,.2f}")
m4.metric("AIC / BIC", f"{aic:,.0f} / {bic:,.0f}")

fig, ax = plt.subplots(figsize=(11, 4.6))
ax.plot(hist.iloc[-250:], color="black", lw=1.3, label="History")
ax.plot(fc["forecast"], color="tab:green", lw=2, label="Forecast")
ax.fill_between(fc.index, fc["lower_95"], fc["upper_95"], color="tab:green", alpha=0.2, label="95% interval")
ax.set_ylabel(f"{karat} gold (INR / gram)"); ax.grid(alpha=0.3); ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)
plt.close(fig)

left, right = st.columns([3, 2])
with left:
    st.subheader(f"{karat} forecast (₹ per gram)")
    st.dataframe(fc.round(2), width="stretch", height=300)
    export = fc.rename(columns={"forecast": "forecast_inr_per_gram", "lower_95": "lower_95_inr_per_gram", "upper_95": "upper_95_inr_per_gram"}).round(2)
    export["karat"] = karat
    export["usd_inr"] = rate
    export["fx_date"] = rate_date
    st.download_button("Download forecast CSV", export.to_csv().encode("utf-8-sig"), f"gold_forecast_{karat}_INR_per_gram.csv", "text/csv")
with right:
    st.subheader("Model notes")
    st.write(f"**Data:** {source}  \n**Observations:** {len(hist):,}  \n**Order:** ({int(p)},{int(d)},{int(q)}) + drift")
    if (uploaded is None and meta.get("test_rmse_model") and ticker == meta.get("ticker")
            and [int(p), int(d), int(q)] == meta.get("order")):
        st.caption(f"Archived notebook evaluation ending {meta.get('test_end', meta.get('trained_until', 'unknown'))}; current refit may differ.")
        st.write(f"**Hold-out RMSE (original USD/oz model):** model {meta['test_rmse_model']:.2f} vs naive {meta['test_rmse_naive']:.2f} USD/oz "
                 f"(last {meta.get('test_days', '₹')} trading days, from the notebook)")
    st.info("Daily gold is close to a random walk: expect the point forecast to be ≈ today's price plus a small drift. "
            "The value of the model is the **uncertainty interval**, which widens with the horizon.")

st.subheader("Compare all gold purities")
rows = []
all_karats = pd.DataFrame(index=usd_fc.index)
for label, purity in FINENESS.items():
    factor = float(rate) * purity / GRAMS_PER_TROY_OUNCE
    rows.append({"Purity": label, "Gold content (%)": purity * 100,
                 "Last close (INR/g)": usd_last * factor,
                 f"Forecast in {horizon} days (INR/g)": float(usd_fc["forecast"].iloc[-1]) * factor,
                 "Lower 95% (INR/g)": float(usd_fc["lower_95"].iloc[-1]) * factor,
                 "Upper 95% (INR/g)": float(usd_fc["upper_95"].iloc[-1]) * factor})
    all_karats[f"{label}_forecast_inr_per_gram"] = usd_fc["forecast"] * factor
all_karats["usd_inr"] = rate
all_karats["fx_date"] = rate_date
st.dataframe(pd.DataFrame(rows).round(2), hide_index=True, width="stretch")
st.download_button("Download all karat forecasts", all_karats.round(4).to_csv().encode("utf-8-sig"), "gold_forecast_all_karats_INR_per_gram.csv", "text/csv")
with st.expander("How prices are converted"):
    st.write("INR per gram = USD per troy ounce x USD-INR / 31.1034768 x fineness.")
    st.write("The same gold forecast is adjusted for purity; these are not four independently trained models. 24K here means fine gold at 999 fineness.")
    st.markdown("Sources: [BIS gold fineness grades](https://lims.bis.gov.in/home/search_is_number/?is_number__doc_no=1417), [NIST unit conversion](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8).")
st.caption("Educational project - not financial advice.")
