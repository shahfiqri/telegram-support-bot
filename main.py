import json
import logging
import telegram
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import openai
import tracking_api
import log_google_sheets
import config
import re

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SOP from JSON
with open('sop.json', 'r', encoding='utf-8') as f:
    SOP_DATA = json.load(f)

def find_sop_reply(message: str):
    """Cari jawapan dalam SOP berdasarkan keyword."""
    for keyword, reply in SOP_DATA.items():
        if keyword.lower() in message.lower():
            return reply
    return None

def chatgpt_reply(message: str):
    """Gunakan OpenAI GPT API jika tiada jawapan dalam SOP."""
    openai.api_key = config.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response['choices'][0]['message']['content']

def extract_tracking_number(message: str):
    """Cari nombor tracking dalam mesej."""
    match = re.search(r'\b([A-Za-z0-9]{8,})\b', message)
    return match.group(1) if match else None

def handle_message(update: Update, context: CallbackContext):
    """Fungsi utama untuk menangani mesej pengguna."""
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Semak jika mesej mengandungi nombor tracking
    tracking_number = extract_tracking_number(user_message)
    if tracking_number:
        result = tracking_api.track(tracking_number)
        context.bot.send_message(chat_id=chat_id, text=result)
        return

    # Cari jawapan dalam SOP
    reply = find_sop_reply(user_message)
    if not reply:
        reply = chatgpt_reply(user_message)
    
    # Hantar jawapan
    context.bot.send_message(chat_id=chat_id, text=reply)
    
    # Log soalan dan jawapan ke Google Sheets
    log_google_sheets.log_message(chat_id, user_message, reply)

def main():
    """Fungsi utama untuk memulakan bot."""
    updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

