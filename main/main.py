import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def plot_price(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Close"])
    plt.title(f"{ticker} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    ticker = "AAPL"
    data = fetch_stock_data(ticker)
    plot_price(data, ticker)
