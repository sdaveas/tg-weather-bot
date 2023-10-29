import asyncio
import sys
import config

from _calendar import get_calendar_events
from _forecast import get_weather_forecast, format_weather_message
from _telegram import send_message_forecast


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

    forecast = get_weather_forecast(config.LAT, config.LON)
    message = format_weather_message(events[0], forecast)

    asyncio.run(send_message_forecast(message))


main()
