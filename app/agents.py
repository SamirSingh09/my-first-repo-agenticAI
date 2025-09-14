from autogen import AssistantAgent, UserProxyAgent
from app.config import settings

def get_agents():
    # Trip Planner Agent
    planner = AssistantAgent(
        name="trip_planner",
        llm_config={
            "config_list": [
                {"model": settings.Model, "api_key": settings.OPENAI_API_KEY}
            ]
        },
        max_consecutive_auto_reply=3,
        system_message="You are a professional travel planner. Always respond in JSON with keys: destination, days, highlights, recommended_hotels, transport."
    )

    # Weather Agent
    weather = AssistantAgent(
        name="weather_agent",
        llm_config={
            "config_list": [
                {"model": settings.Model, "api_key": settings.OPENAI_API_KEY}
            ]
        },
        max_consecutive_auto_reply=3,
        system_message="You are a weather expert. Respond in JSON with keys: destination, forecast (list of daily weather summaries)."
    )

    # Budget Agent
    budget = AssistantAgent(
        name="budget_agent",
        llm_config={
            "config_list": [
                {"model": settings.Model, "api_key": settings.OPENAI_API_KEY}
            ]
        },
        max_consecutive_auto_reply=3,
        system_message="You are a budget planner. Respond in JSON with keys: type, estimated_cost_usd, breakdown (dict with flights, hotels, food, activities)."
    )

    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
         code_execution_config={"use_docker": False}
    )

    return planner, weather, budget, user_proxy
