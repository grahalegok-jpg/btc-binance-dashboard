import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.title("Realtime BTC/USDT Price (Binance)")

# Refresh setiap 5 detik (5000 ms)
count = st_autorefresh(interval=5000, limit=None, key="refresh")

def fetch_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = data.get("price")
        if price:
            return float(price)
        else:
            return None
    except:
        return None

price = fetch_price()
if price:
    st.metric(label="BTC/USDT Price", value=f"${price:,.2f}")
else:
    st.error("Gagal mengambil data harga.")

