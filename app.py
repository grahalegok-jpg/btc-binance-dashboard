import streamlit as st
import requests
import pandas as pd

def get_ticker():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    res = requests.get(url)
    data = res.json()
    return float(data['price'])

def get_order_book():
    url = "https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=5"
    res = requests.get(url)
    data = res.json()
    bids = [(float(p), float(q)) for p,q in data['bids']]
    asks = [(float(p), float(q)) for p,q in data['asks']]
    return bids, asks

def get_klines(interval='1m', limit=50):
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={interval}&limit={limit}"
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data, columns=[
        "OpenTime","Open","High","Low","Close","Volume",
        "CloseTime","QuoteAssetVolume","NumberOfTrades",
        "TakerBuyBaseAssetVolume","TakerBuyQuoteAssetVolume","Ignore"
    ])
    df = df.astype({
        "Open":float,"High":float,"Low":float,"Close":float,"Volume":float
    })
    return df

def moving_average(series, n):
    return series.rolling(n).mean()

def rsi(series, n=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=n).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def macd(series, n_fast=12, n_slow=26, n_signal=9):
    ema_fast = series.ewm(span=n_fast, adjust=False).mean()
    ema_slow = series.ewm(span=n_slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=n_signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

st.title("Dashboard Realtime BTC/USDT Binance")

price = get_ticker()
st.metric("Harga BTC/USDT", f"${price:,.2f}")

bids, asks = get_order_book()
st.subheader("Order Book (Top 5)")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Bids (Buy Orders)**")
    st.table(pd.DataFrame(bids, columns=["Price", "Quantity"]))
with col2:
    st.markdown("**Asks (Sell Orders)**")
    st.table(pd.DataFrame(asks, columns=["Price", "Quantity"]))

df = get_klines()
df["MA5"] = moving_average(df["Close"], 5)
df["MA10"] = moving_average(df["Close"], 10)
df["RSI"] = rsi(df["Close"])
macd_line, signal_line, hist = macd(df["Close"])
df["MACD"] = macd_line
df["Signal"] = signal_line

st.subheader("Indikator Teknikal (1m candle)")
st.write(f"MA5: {df['MA5'].iloc[-1]:.2f} | MA10: {df['MA10'].iloc[-1]:.2f} | RSI: {df['RSI'].iloc[-1]:.2f}")
st.write(f"MACD: {df['MACD'].iloc[-1]:.2f} | Signal: {df['Signal'].iloc[-1]:.2f}")

st.info("Reload halaman ini untuk update data realtime.")
