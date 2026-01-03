import numpy as np

def compute_daily_returns(data):
    return data["Close"].pct_change().dropna()

def rolling_volatility(returns, window=20):
    return returns.rolling(window).std() * np.sqrt(252)

def forecast_volatility(returns, window=20):
    # Simple & valid: use recent rolling volatility
    vol = rolling_volatility(returns, window)
    return float(vol.iloc[-1])
