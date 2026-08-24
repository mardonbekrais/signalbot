import logging
import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render URL
WEBAPP_URL = "https://signalbot-z9lk.onrender.com"

# Keep-alive task to prevent Render from sleeping
async def keep_alive():
    while True:
        logging.info("Keep-alive pinging self...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(WEBAPP_URL) as response:
                    logging.info(f"Pinged {WEBAPP_URL}, status: {response.status}")
        except Exception as e:
            logging.error(f"Ping failed: {e}")
        await asyncio.sleep(300) # Ping every 5 minutes

@dp.message(Command("start"))
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 TIMA • SIGNAL BOT'ni ochish", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer("Salom! Quyidagi tugma orqali botimizga kiring:", reply_markup=markup)

async def main():
    # Start polling and keep-alive task
    asyncio.create_task(keep_alive())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
