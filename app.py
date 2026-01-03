import streamlit as st  #for UI (seems a good fir for now, can explore others later)
import plotly.graph_objects as go 
import requests
import pandas as pd
import numpy as np

#layouts 

st.set_page_config(page_title="Financial Risk Dashboard", layout="wide")
st.title("Financial Risk Forecasting System")

# Fine for now, have to figure out a way to source the tickers from the db or an api instead of hardcoding
STOCKS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Meta": "META"
}

#creating boxes for user inputs (check with malhar if more inputs are needed)
company = st.selectbox("Select a stock", list(STOCKS.keys()))
ticker = STOCKS[company]

period = st.text_input("Time period (e.g. 1y, 6mo, max)", value="1y")


#defining the api endpoints to fetch data from backend
prices_res = requests.get(
    "http://127.0.0.1:8000/prices",
    params={"ticker": ticker, "period": period}
)

vol_res = requests.get(
    "http://127.0.0.1:8000/volatility",
    params={"ticker": ticker, "period": period}
)

if prices_res.status_code != 200 or vol_res.status_code != 200:
    st.error("Backend error while fetching data")
    st.stop()

prices = pd.DataFrame(prices_res.json())
prices["Date"] = pd.to_datetime(prices["Date"])

vol = vol_res.json()

st.metric(
    label="Forecasted Volatility",
    value=f"{vol['forecasted_volatility']:.2%}",
    delta=f"Risk: {vol['risk_level']}"
)

prices["Returns"] = prices["Close"].pct_change()

rolling_vol = prices["Returns"].rolling(window=30).std() * np.sqrt(252)

annual_vol = prices["Returns"].std() * np.sqrt(252) * 100
avg_return = prices["Returns"].mean() * 100

cum_returns = (1 + prices["Returns"]).cumprod()
drawdown = (cum_returns / cum_returns.cummax() - 1).min() * 100

c1, c2, c3 = st.columns(3)
c1.metric("Annualized Volatility", f"{annual_vol:.2f}%")
c2.metric("Avg Daily Return", f"{avg_return:.2f}%")
c3.metric("Max Drawdown", f"{drawdown:.2f}%")

price_fig = go.Figure()
price_fig.add_trace(go.Scatter(
    x=prices["Date"],
    y=prices["Close"],
    mode="lines",
    name="Close Price"
))
price_fig.update_layout(
    title=f"{company} Price",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    hovermode="x unified"
)

vol_fig = go.Figure()
vol_fig.add_trace(go.Scatter(
    x=prices["Date"],
    y=rolling_vol,
    mode="lines",
    name="30-Day Rolling Volatility"
))
vol_fig.update_layout(
    title="Rolling Volatility (Risk)",
    xaxis_title="Date",
    yaxis_title="Volatility",
    hovermode="x unified"
)

st.plotly_chart(price_fig, use_container_width=True)
st.plotly_chart(vol_fig, use_container_width=True)
