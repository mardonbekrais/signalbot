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

# ...

# Serve static files from 'webapp' directory
async def handle_static(request):
    path = request.match_info.get('tail', '')
    if not path or path == '/':
        path = 'index.html'
    # Path is relative to the root (where bot.py is), 
    # but based on the Render settings, we need to find the 'webapp' folder correctly.
    # If the root is 'Signal', webapp is 'webapp/'. 
    # Let's try an absolute path or relative path from the script location.
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "webapp", path)
    
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    return web.Response(text=f"File not found: {file_path}", status=404)

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

