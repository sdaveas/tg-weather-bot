from googleapiclient.discovery import build
from datetime import datetime, timedelta
import config


def main():
    print(get_calendar_events())


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


main()
