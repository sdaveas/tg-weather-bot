import requests
import config

from datetime import datetime
import time


def get_weather_forecasts(lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": f"{lat}",
        "lon": f"{lon}",
        "appid": config.OW_API_KEY,
        "units": "metric",
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    return response.json()


def get_closest_forecast(forecasts, event_time):
    date_time_obj = datetime.fromisoformat(event_time)
    event_unix_timestamp = int(date_time_obj.timestamp())
    print("unix_timestamp:", event_unix_timestamp)

    forecasts = get_weather_forecasts(config.LAT, config.LON)

    msg = ""

    closest_forecast = forecasts["list"][0]
    for forecast in forecasts["list"]:
        if forecast["dt"] + 3 * 60 * 60 >= event_unix_timestamp:
            closest_forecast = forecast
            break

    return closest_forecast


def bad_weather(message):
    return "rain" in message or "thunderstorm" in message or "snow" in message


def format_weather_message(event, forecast):
    temperature = forecast["main"]["temp"]
    temperature_feel = forecast["main"]["feels_like"]
    humidity = forecast["main"]["humidity"]
    description = forecast["weather"][0]["description"]

    summary = event["summary"]
    start_time = datetime.fromisoformat(event["start"]).strftime("%A %H:%M")
    forecast_time = datetime.fromtimestamp(forecast["dt"]).strftime("%H:%M")
    location = event["location"] if event["location"] != "" else "Athens"

    message = f"Weather forecast for {summary} at {start_time} (forecast for {forecast_time}) in {location}:\n\n Temperature: {temperature}°C - feels like {temperature_feel}°C\n Humidity: {humidity}%\n Description: {description}\n"

    return message
