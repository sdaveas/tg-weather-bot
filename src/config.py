import os
import dotenv

ENV_FILE = "../config/local.env"

if os.path.exists(ENV_FILE):
    dotenv.load_dotenv(ENV_FILE)

# Telegram
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# OpenWeatherMap
OW_API_KEY = os.getenv("OW_API_KEY")

# Google Calendar
GC_API_KEY = os.getenv("GC_API_KEY")
GC_ID = os.getenv("GC_ID")
GC_TIMEDELTA_HOURS = os.getenv("GC_TIMEDELTA_HOURS")

# Location
LAT = os.getenv("LAT")
LON = os.getenv("LON")
