import os
import dotenv

ENV_FILE='local.env'

if os.path.exists(ENV_FILE):
    dotenv.load_dotenv(ENV_FILE)

# Telegram
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

# OpenWeatherMap
OW_API_KEY = os.getenv('OW_API_KEY')