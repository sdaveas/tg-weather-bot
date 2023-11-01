import asyncio
import sys
import config

from _calendar import get_calendar_events
from _forecast import get_weather_forecasts, format_weather_message, bad_weather
from _telegram import send_message_forecast


def main():
    dry_run = False
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        dry_run = True

    events = get_calendar_events()
    if len(events) == 0:
        print("No events found")
        return
    

    forecast = get_weather_forecasts(config.LAT, config.LON)
    message = format_weather_message(events[0], forecast)

    if not bad_weather(message):
        print("today it's a good weather, skipping publishing message")
        print(message)
        return

    if dry_run:
        print(message)
        return

    asyncio.run(send_message_forecast(message))


main()
