import asyncio
import datetime
import requests
from telegram import Bot
from telegram.ext import Updater
from apscheduler.schedulers.blocking import BlockingScheduler

import config

# Create bot instance
bot = Bot(token=config.TG_BOT_TOKEN)

# TODO: less inconvenient way to get chat ID
# updates = asyncio.run(bot.get_updates())
# chat_id = updates[-1].message.chat_id

# coords of our tennis court https://www.google.com/maps/@38.0166107,23.7793641,673m/data=!3m1!1e3?entry=ttu
LAT = 38.016630
LON = 23.780721

# fetch weather forecast for tennis court
def get_weather_forecast():
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={config.OW_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

# format weather forecast data into a message
def format_weather_message(data):
    # Extract relevant data from the API response
    temperature = data['main']['temp']
    temperature_feel = data['main']['feels_like']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    # Create the message string
    message = f"Weather forecast for Athens:\n\n Temperature: {temperature}°C - feels like {temperature_feel}°C\n Humidity: {humidity}%\n Description: {description}"

    return message

# send weather forecast message
async def send_weather_forecast():
    data = get_weather_forecast()
    message = format_weather_message(data)
    await bot.send_message(chat_id=config.TG_CHAT_ID, text=message)

asyncio.run(send_weather_forecast())
