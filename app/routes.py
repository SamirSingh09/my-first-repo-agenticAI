from fastapi import APIRouter, HTTPException
from app.models import TripRequest, TripResponse, Itinerary, WeatherReport, BudgetEstimate
from app.agents import get_agents
import json
import logging
import re 

router = APIRouter()
planner, weather_agent, budget_agent, user_proxy = get_agents()
logger = logging.getLogger(__name__)

def extract_text(result):
    """Get plain text from Autogen ChatResult or str"""
    if isinstance(result, str):
        return result
    if hasattr(result, "response_text"):
        return result.response_text
    return str(result)
def safe_json_parse(response: str):
    """Extract JSON safely from LLM response"""
    try:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(response)
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e} | Raw: {response}")
        raise HTTPException(status_code=500, detail="Invalid JSON returned by AI agent")

def normalize_itinerary(data: dict):
    """Ensure itinerary fields are in the correct format"""
    if isinstance(data.get("recommended_hotels"), str):
        data["recommended_hotels"] = [data["recommended_hotels"]]
    return data
def normalize_weather(data: dict):
    """Normalize weather fields to match WeatherReport model"""
    forecast = []
    for item in data.get("forecast", []):
        if isinstance(item, dict):
            forecast.append({
                "date": item.get("date") or item.get("day") or "Unknown",
                "summary": item.get("summary") or item.get("weather") or "N/A",
                "temperature": item.get("temperature") or item.get("details") or "N/A"
            })
        else:
            # If it's already a string, just wrap it
            forecast.append({
                "date": "Unknown",
                "summary": str(item),
                "temperature": "N/A"
            })
    data["forecast"] = forecast
    return data


@router.post("/plan_trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    try:
        logger.info(f"Received trip prompt: {request.prompt}")

        # 1. Itinerary
        itinerary_result =planner.generate_reply(messages=[{"role": "user", "content": request.prompt}])
        itinerary = normalize_itinerary(safe_json_parse(extract_text(itinerary_result)))

        # 2. Weather
        weather_prompt = f"Give me a 5-day weather forecast for {itinerary['destination']}."
        weather_result = weather_agent.generate_reply(messages=[{"role": "user", "content": weather_prompt}])
        weather = normalize_weather(safe_json_parse(extract_text(weather_result)))

        # 3. Budget
        budget_prompt = f"Estimate a {request.budget_type} budget for a {itinerary['days']}-day trip to {itinerary['destination']}."
        budget_result =budget_agent.generate_reply(messages=[{"role": "user", "content": budget_prompt}])
        budget = normalize_itinerary(safe_json_parse(extract_text(budget_result)))

        return TripResponse(
            itinerary=Itinerary(**itinerary),
            weather=WeatherReport(**weather),
            budget=BudgetEstimate(**budget)
        )

    except Exception as e:
        logger.error(f"Trip planning failed: {e}")
        raise HTTPException(status_code=500, detail="Error generating trip plan")
