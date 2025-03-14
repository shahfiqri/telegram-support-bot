import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

def authorize_google_sheets():
    """Authorize access to Google Sheets."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("telegram-bot-logging-406b3514ac88.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(config.GOOGLE_SHEET_ID).sheet1

def log_message(chat_id, user_message, bot_reply):
    """Log conversation data to Google Sheets."""
    sheet = authorize_google_sheets()
    sheet.append_row([str(chat_id), user_message, bot_reply])
