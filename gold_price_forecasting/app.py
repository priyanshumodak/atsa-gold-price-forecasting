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

st.set_page_config(page_title="Gold Price Forecaster", page_icon="🪙", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
META_PATH = BASE_DIR / "models/model_meta.json"
CSV_PATH = BASE_DIR / "data/gold_daily.csv"
meta = json.loads(META_PATH.read_text()) if META_PATH.exists() else {}


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
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker", meta.get("ticker", "GC=F"), help="GC=F = COMEX gold futures, GLD = gold ETF")
years = st.sidebar.slider("History (years)", 3, 15, 10)
horizon = st.sidebar.slider("Forecast horizon (business days)", 5, 60, 30)
d_p, d_d, d_q = meta.get("order", [0, 1, 0])
c1, c2, c3 = st.sidebar.columns(3)
p = c1.number_input("p", 0, 5, int(d_p))
d = c2.number_input("d", 1, 2, int(d_d))
q = c3.number_input("q", 0, 5, int(d_q))
st.sidebar.caption("Prices are USD per troy ounce for GC=F; GLD uses USD per share. Dates include weekdays and may include exchange holidays.")
st.sidebar.caption("Order defaults to the model chosen by BIC in the notebook.")

# ---------------------------------------------------------------- main
st.title("🪙 Daily Gold Price Forecaster")
st.caption("Applied Time Series Analysis · ARIMA(p,d,q) on log price; exponentiated forecasts are medians")

uploaded = st.sidebar.file_uploader("Or upload gold price CSV", type=["csv"], help="Columns: Date, Close. Positive prices with at least 100 observations.")
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
last = float(hist.iloc[-1])
end = float(fc["forecast"].iloc[-1])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Last close (source units)", f"{last:,.2f}", help=f"as of {hist.index[-1].date()}")
m2.metric(f"Forecast in {horizon} days", f"{end:,.2f}", f"{(end / last - 1) * 100:+.2f}%")
m3.metric("95% interval at horizon", f"{fc['lower_95'].iloc[-1]:,.0f} – {fc['upper_95'].iloc[-1]:,.0f}")
m4.metric("AIC / BIC", f"{aic:,.0f} / {bic:,.0f}")

fig, ax = plt.subplots(figsize=(11, 4.6))
ax.plot(hist.iloc[-250:], color="black", lw=1.3, label="History")
ax.plot(fc["forecast"], color="tab:green", lw=2, label="Forecast")
ax.fill_between(fc.index, fc["lower_95"], fc["upper_95"], color="tab:green", alpha=0.2, label="95% interval")
ax.set_ylabel("Price (source units)"); ax.grid(alpha=0.3); ax.legend()
ax.spines[["top", "right"]].set_visible(False)
st.pyplot(fig)

left, right = st.columns([3, 2])
with left:
    st.subheader("Forecast table")
    st.dataframe(fc.round(2), width="stretch", height=300)
    st.download_button("Download forecast CSV", fc.round(2).to_csv().encode(), "gold_forecast.csv", "text/csv")
with right:
    st.subheader("Model notes")
    st.write(f"**Data:** {source}  \n**Observations:** {len(hist):,}  \n**Order:** ({int(p)},{int(d)},{int(q)}) + drift")
    if (uploaded is None and meta.get("test_rmse_model") and ticker == meta.get("ticker")
            and [int(p), int(d), int(q)] == meta.get("order")):
        st.caption(f"Archived notebook evaluation ending {meta.get('test_end', meta.get('trained_until', 'unknown'))}; current refit may differ.")
        st.write(f"**Hold-out RMSE:** model {meta['test_rmse_model']:.2f} vs naive {meta['test_rmse_naive']:.2f} USD "
                 f"(last {meta.get('test_days', '?')} trading days, from the notebook)")
    st.info("Daily gold is close to a random walk: expect the point forecast to be ≈ today's price plus a small drift. "
            "The value of the model is the **uncertainty interval**, which widens with the horizon.")

st.caption("Educational project — not financial advice.")
