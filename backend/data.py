import yfinance as yf

def get_price_data(ticker: str, period: str = "1y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)

    if data.empty:
        raise ValueError("No data found")

    return data
