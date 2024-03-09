from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from TelegramBot import handlers
from TelegramBot import config

class TelegramBot:
    def __init__(self):
        self.TOKEN = config.Config.TELEGRAM_BOT_TOKEN

    def launch_bot(self):
        app = Application.builder().token(self.TOKEN).build()

        app.add_handler(CommandHandler('start', self.start_command))
        app.add_handler(CommandHandler('help', self.help_command))

        app.add_handler(MessageHandler(filters.TEXT, handlers.handle_message))

        app.add_error_handler(self.error)

        app.run_polling(poll_interval=3)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Test")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Test")

    # errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')
