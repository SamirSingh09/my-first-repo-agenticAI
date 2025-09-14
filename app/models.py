from pydantic import BaseModel
from typing import List, Optional

class TripRequest(BaseModel):
    prompt: str
    budget_type: Optional[str] = "mid"   # budget | mid | luxury

class TransportInfo(BaseModel):
    from_airport: str
    local_travel: str
    notes: str | None = None

class Itinerary(BaseModel):
    destination: str
    days: int
    activities: List[str]
    recommended_hotels: List[str]
    transport: TransportInfo   # ✅ structured

class ForecastItem(BaseModel):
    date: str
    summary: str
    temperature: str

class WeatherReport(BaseModel):
    forecast: List[ForecastItem]

class BudgetEstimate(BaseModel):
    type: str
    estimated_cost_usd: int
    breakdown: dict

class TripResponse(BaseModel):
    itinerary: Itinerary
    weather: WeatherReport
    budget: BudgetEstimate




