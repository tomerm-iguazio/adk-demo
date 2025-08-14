from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import mlrun
import requests


def get_restaurants_reviews():
    project = mlrun.get_or_create_project("adk-project")
    restaurant_reviews_artifact = project.get_artifact("restaurants_reviews")
    df = restaurant_reviews_artifact.to_dataitem().as_df()

    return {
        "status": "success",
        "data": df.to_dict("records")
    }


def get_restaurants_sanitation_reports():
    project = mlrun.get_or_create_project("adk-project")
    restaurant_sanitation_reports_artifact = project.get_artifact("restaurants_sanitation_reports")
    df = restaurant_sanitation_reports_artifact.to_dataitem().as_df()

    return {
        "status": "success",
        "data": df.to_dict("records")
    }


def get_restaurants_locations():
    return {"status": "success", "data": {"Grillland": "Tel Aviv", "slicevana": "herzliya", "Noodletopia": "Ramat Gan"}}


def get_weather_by_city(city_name: str):
    # Step 1: Geocode city name to lat/lon using OpenStreetMap Nominatim
    geo_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    try:
        geo_resp = requests.get(geo_url, params=geo_params, headers={"User-Agent": "agent-app"}, timeout=5)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data:
            return {"status": "error", "message": f"City '{city_name}' not found"}

        lat = float(geo_data[0]["lat"])
        lon = float(geo_data[0]["lon"])

    except requests.RequestException as e:
        return {"status": "error", "message": f"Geocoding failed: {e}"}

    # Step 2: Fetch weather from Open-Meteo
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    try:
        weather_resp = requests.get(weather_url, params=weather_params, timeout=5)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        if "current_weather" not in weather_data:
            return {"status": "error", "message": "No weather data available"}

        return {
            "status": "success",
            "city": city_name,
            "coordinates": {"lat": lat, "lon": lon},
            "weather": weather_data["current_weather"]
        }

    except requests.RequestException as e:
        return {"status": "error", "message": f"Weather fetch failed: {e}"}


root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o-mini"),
    name="restaurant_insights_agent",
    description="Provides restaurant reviews, sanitation reports, and weather info by city.",
    instruction="""
    Use the available tools to fetch restaurant reviews and sanitation reports. Additionally, you can provide weather
    information.
    Always provide exactly what is requested, without unnecessary references to other topics or unrelated information.
    Make the response clean and user-friendly.
    Make sure you review the conversation history to understand the context.
    """,
    tools=[get_restaurants_reviews, get_restaurants_sanitation_reports, get_weather_by_city, get_restaurants_locations],
)
