import streamlit as st
import requests
import time

st.title("Realtime BTC/USDT Price (Binance)")

placeholder = st.empty()

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

# Loop update harga setiap 5 detik
while True:
    price = fetch_price()
    if price:
        placeholder.metric(label="BTC/USDT Price", value=f"${price:,.2f}")
    else:
        placeholder.error("Gagal mengambil data harga.")
    time.sleep(5)import streamlit as st
import requests

