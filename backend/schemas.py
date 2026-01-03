

from pydantic import BaseModel

class VolatilityResponse(BaseModel):
    ticker: str
    period: str
    forecasted_volatility: float
    risk_level: str
