from telethon import TelegramClient, events, Button
import asyncio
import logging
from bot.config import API_ID, API_HASH, BOT_TOKEN

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot client
client = TelegramClient('bot', API_ID, API_HASH)

# State to store user inputs
user_states = {}

def get_auth_keyboard(current_code=""):
    code_display = " ".join([c if c != "" else "_" for c in (current_code.ljust(5, "_"))])
    buttons = [
        [Button.inline(str(i), f"digit_{i}") for i in range(1, 4)],
        [Button.inline(str(i), f"digit_{i}") for i in range(4, 7)],
        [Button.inline(str(i), f"digit_{i}") for i in range(7, 10)],
        [Button.inline("🗑️", "clear"), Button.inline("0", "digit_0"), Button.inline("✅", "done")]
    ]
    return buttons, code_display

def get_main_menu():
    buttons = [
        [Button.inline("📩 XABAR YUBORISH", "send_message")],
        [Button.inline("👥 Guruhlarni boshqarish", "groups"), Button.inline("📝 Shablonlar", "templates")],
        [Button.inline("⚙️ Sozlamalar", "settings")]
    ]
    return buttons

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Salom! Akkountni ulash uchun telefon raqamingizni yuboring (+998xxxxxxxxx):")
    user_states[event.sender_id] = {'step': 'awaiting_phone'}

@client.on(events.NewMessage)
async def handle_messages(event):
    if event.text.startswith('/'): return # Commands are handled elsewhere

    user_id = event.sender_id
    if user_id in user_states:
        state = user_states[user_id]
        
        if state.get('step') == 'awaiting_phone':
            phone = event.text.strip()
            if not phone.startswith('+'):
                await event.respond("Iltimos, telefon raqamini xalqaro formatda kiriting (masalan, +998901234567):")
                return

            logger.info(f"DEBUG: Phone: '{phone}', Type: {type(phone)}")
            
            # Trigger real code request via Telegram API
            try:
                # We need a phone_code_hash for sign_in later
                phone_code_hash = await client.send_code_request(phone)
                user_states[user_id] = {
                    'step': 'awaiting_code', 
                    'phone': phone, 
                    'code': "", 
                    'phone_code_hash': phone_code_hash.phone_code_hash
                }
                buttons, code_display = get_auth_keyboard("")
                await event.respond("Telegram'ga kod yuborildi. Kodni quyidagi tugmalar orqali kiriting:", buttons=buttons)
            except Exception as e:
                logger.error(f"DEBUG: Error in send_code_request: {e}", exc_info=True)
                await event.respond(f"Xatolik yuz berdi: {e}")
                del user_states[user_id]

@client.on(events.CallbackQuery)
async def handle_callback(event):
    user_id = event.sender_id
    if user_id not in user_states: return

    data = event.data.decode()
    state = user_states[user_id]

    if data.startswith('digit_'):
        digit = data.split('_')[1]
        if len(state['code']) < 5:
            state['code'] += digit
    elif data == 'clear':
        state['code'] = ""
    elif data == 'done':
        # Finalize auth with the real code
        try:
            logger.info(f"DEBUG: Sign In - Phone: {state['phone']}, Code: {state['code']}, Hash: {state['phone_code_hash']}")
            await client.sign_in(phone=state['phone'], code=state['code'], phone_code_hash=state['phone_code_hash'])
            await event.edit(f"✅ Akkount muvaffaqiyatli ulandi!\n\n🚀 ASOSIY MENYU", buttons=get_main_menu())
            user_states[user_id] = {'step': 'main_menu'}
        except Exception as e:
            logger.error(f"DEBUG: Error in sign_in: {e}", exc_info=True)
            await event.respond(f"Kod noto'g'ri yoki xatolik yuz berdi: {e}")
            state['code'] = "" # Reset code
            buttons, _ = get_auth_keyboard("")
            await event.edit("Kod xato! Qayta urinib ko'ring:", buttons=buttons)
        return
    elif data == 'send_message':
        await event.edit("📩 Xabar yuborish rejimiga o'tildi. Xabar matnini yuboring:")
        state['step'] = 'awaiting_message_text'
        return
    
    if state['step'] == 'awaiting_code':
        buttons, code_display = get_auth_keyboard(state['code'])
        await event.edit(f"🔢 Kiritilgan: {code_display}", buttons=buttons)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    logger.info("Bot ishga tushdi...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
