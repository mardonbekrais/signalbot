import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Replace with your actual WebApp URL (e.g., ngrok URL or hosted URL)
WEBAPP_URL = "https://poor-hats-work.loca.lt"


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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
