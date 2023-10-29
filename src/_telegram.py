import config
from telegram import Bot


async def send_message_forecast(message):
    bot = Bot(token=config.TG_BOT_TOKEN)

    await bot.send_message(chat_id=config.TG_CHAT_ID, text=message)
