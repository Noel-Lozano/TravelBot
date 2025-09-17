import os
import requests
from datetime import datetime

WEATHER_KEY = os.environ.get("WEATHER_KEY")
if not WEATHER_KEY:
    raise ValueError("WEATHER_KEY environment variable is not set.")

def get_weather(city, date=None):
    """
    Fetches weather forecast for a given city on a specific date using OpenWeatherMap 5-day forecast API.
    
    - city: city name (str)
    - date: YYYY-MM-DD (str). If None or today, returns the nearest forecast.

    Returns a string like "scattered clouds, 22°C".
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "list" not in data:
            return "moderate"

        # If no date provided, default to today
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        target_date = datetime.strptime(date, "%Y-%m-%d")

        # Find the forecast closest to noon of that date
        best_match = None
        min_diff = float("inf")

        for entry in data["list"]:
            forecast_time = datetime.fromtimestamp(entry["dt"])
            diff = abs((forecast_time - target_date).total_seconds())

            if diff < min_diff:
                min_diff = diff
                best_match = entry

        if best_match:
            description = best_match["weather"][0]["description"]
            temp = best_match["main"]["temp"]
            return f"{description}, {temp}°C"
        else:
            return "moderate"

    except Exception as e:
        print(f"[ERROR] Weather lookup failed: {e}")
        return "moderate"
