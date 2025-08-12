import streamlit as st
import requests

st.title("Harga BTC/USDT")

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data.get("price", 0))
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return None
       
