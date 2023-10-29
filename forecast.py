import asyncio
import datetime
import requests
import sys

from telegram import Bot

from apscheduler.schedulers.blocking import BlockingScheduler

from googleapiclient.discovery import build
from google.oauth2 import service_account

from datetime import datetime, timedelta

import config


def main():
    dry_run = False
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        dry_run = True

    events = get_calendar_events()
    if len(events) == 0:
        print("No events found")
        return

    if dry_run:
        print(events[0])
        return

    asyncio.run(send_weather_forecast(events[0], config.LAT, config.LON))


def get_calendar_events():
    timedelta_hours = int(config.GC_TIMEDELTA_HOURS)

    service = build("calendar", "v3", developerKey=config.GC_API_KEY)

    matching_events = []

    start_date = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end_date = (datetime.utcnow() + timedelta(hours=timedelta_hours)).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId=config.GC_ID,
            timeMin=start_date,
            timeMax=end_date,
        )
        .execute()
    )

    events = events_result.get("items", [])
    for event in events:
        matching_events.append(
            {
                "summary": event["summary"],
                "start": event["start"].get("dateTime", event["start"].get("date")),
                "location": event["location"],
            }
        )

    return matching_events


async def send_weather_forecast(event, lat, lon):
    bot = Bot(token=config.TG_BOT_TOKEN)

    forecast = get_weather_forecast(lat, lon)
    message = format_weather_message(event, forecast)

    await bot.send_message(chat_id=config.TG_CHAT_ID, text=message)


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


main()
