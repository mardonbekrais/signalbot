import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Convert API_ID to int explicitly
api_id_raw = os.getenv("API_ID")
API_ID = int(api_id_raw) if api_id_raw else None
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("API_ID, API_HASH yoki BOT_TOKEN o'zgaruvchilari .env faylida topilmadi!")
