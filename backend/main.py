from fastapi import FastAPI, HTTPException
from backend.data import get_price_data
from backend.volatility import compute_daily_returns, forecast_volatility
from backend.schemas import VolatilityResponse

app = FastAPI(title="Financial Risk API")


@app.get("/")
def root():
    return {"status": "Backend is running"}


@app.get("/prices")
def get_prices(ticker: str, period: str):
    data = get_price_data(ticker, period)

    data = data.reset_index()  # CRITICAL LINE
    data["Date"] = data["Date"].astype(str)

    return data.to_dict(orient="records")



def risk_label(vol):
    if vol < 0.2:
        return "Low"
    elif vol < 0.4:
        return "Medium"
    else:
        return "High"


@app.get("/volatility", response_model=VolatilityResponse)
def get_volatility_endpoint(ticker: str, period: str = "1y"):
    try:
        # Step 1: Get price data
        data = get_price_data(ticker, period)

        # Step 2: Compute returns
        returns = compute_daily_returns(data)

        #Step 3: Forecast volatility
        vol = forecast_volatility(returns)

        # Step 4: Return structured response
        return VolatilityResponse(
            ticker=ticker,
            period=period,
            forecasted_volatility=round(vol, 4),
            risk_level=risk_label(vol)
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
