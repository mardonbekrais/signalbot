import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv
from aiohttp import web

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render URL
WEBAPP_URL = "https://signalbot-z9lk.onrender.com"

@dp.message(Command("start"))
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 TIMA • SIGNAL BOT'ni ochish", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer("Salom! Quyidagi tugma orqali botimizga kiring:", reply_markup=markup)

# Serve static files from 'webapp' directory
async def handle_static(request):
    path = request.match_info.get('tail', 'index.html')
    # Path is relative to the root, but inside 'webapp' folder
    # Since Root Directory on Render is set to 'Signal', webapp path is 'webapp/'
    file_path = os.path.join("webapp", path)
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    return web.Response(text="File not found", status=404)

async def start_web_server():
    app = web.Application()
    # Route for static files
    app.router.add_get('/{tail:.*}', handle_static)
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Web server started on port {port}")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

