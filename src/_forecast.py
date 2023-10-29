import requests
import config


def get_weather_forecast(lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/weather"

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


def format_weather_message(event, forecast):
    temperature = forecast["main"]["temp"]
    temperature_feel = forecast["main"]["feels_like"]
    humidity = forecast["main"]["humidity"]
    description = forecast["weather"][0]["description"]

    location = event["location"] if event["location"] != "" else "Athens"

    message = f"Weather forecast for {location}:\n\n Temperature: {temperature}°C - feels like {temperature_feel}°C\n Humidity: {humidity}%\n Description: {description}"

    return message
