import requests
import config


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


def bad_weather(forecasts):
    description = forecasts[0]["weather"][0]["description"]
    return "rain" in description or "thunderstorm" in description or "snow" in description


def format_weather_message(event, forecasts):
    forecast = forecasts.list[0]
    temperature_feel = forecast["main"]["feels_like"]
    humidity = forecast["main"]["humidity"]
    description = forecast["weather"][0]["description"]

    summary = event["summary"]
    location = event["location"] if event["location"] != "" else "Athens"

    message = f"Weather forecast for {summary} in {location}:\n\n Temperature: {temperature}°C - feels like {temperature_feel}°C\n Humidity: {humidity}%\n Description: {description}"

    return message
