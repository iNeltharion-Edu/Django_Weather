import requests
import pytz
from datetime import datetime
from .models import CityWeather

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TOKEN")
API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

CITIES = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "Rome": "Europe/Rome",
    "Moscow": "Europe/Moscow",
    "Amsterdam": "Europe/Amsterdam",
}


def get_local_time(city, timezone):
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime("%H:%M")


def update_weather():
    for city, timezone in CITIES.items():
        response = requests.get(API_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        })
        data = response.json()

        forecast_response = requests.get(FORECAST_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        })
        forecast_data = forecast_response.json()

        hourly_forecast = []
        daily_forecast = {}

        for item in forecast_data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            hour = dt.strftime("%H:%M")
            temp = item["main"]["temp"]

            if len(hourly_forecast) < 24:
                hourly_forecast.append({"hour": hour, "temp": temp})

            day = dt.strftime("%A")
            if day not in daily_forecast:
                daily_forecast[day] = {
                    "temp_min": round(item["main"]["temp_min"]),
                    "temp_max": round(item["main"]["temp_max"]),
                    "desc": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                }

        CityWeather.objects.update_or_create(
            city=city,
            defaults={
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "time": get_local_time(city, timezone),
                "forecast": {"hourly": hourly_forecast, "daily": daily_forecast}
            }
        )
