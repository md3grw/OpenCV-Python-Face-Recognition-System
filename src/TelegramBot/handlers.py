from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import TelegramBot.config as config

#responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in text:
        return 'hi mate'
    
    return 'wdym'

#messages
async def handle_message(update: Update, context: ContextTypes. DEFAULT_TYPE):
    message_type: str = update.message. chat.type

    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if config.BOT_USERNAME in text:
            new_text: str = text. replace(config.BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)
