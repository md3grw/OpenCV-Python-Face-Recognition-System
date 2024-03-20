from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from TelegramBot import handlers
from TelegramBot import config
import app_config
import os

class TelegramBot:
    def __init__(self):
        self.TOKEN = config.Config.TELEGRAM_BOT_TOKEN

    def launch_bot(self):
        app = Application.builder().token(self.TOKEN).build()

        app.add_handler(CommandHandler('start', self.start_command))
        app.add_handler(CommandHandler('help', self.help_command))
        app.add_handler(CommandHandler('send_video', self.send_video_command))

        app.add_handler(MessageHandler(filters.TEXT, handlers.handle_message))

        app.add_error_handler(self.error)

        app.run_polling(poll_interval=3)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello there! 👋 Welcome to SpectatorBot! I'm here to assist you with operating your videocamera. \nhttps://github.com/md3grw/OpenCV-Python-Face-Recognition-System) \nTo get started, feel free to explore the available commands. If you ever need help, just type /help. Enjoy your time with SpectatorBot!")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Type /send_video to get the videos.\nType /set_longevity (amount of second) to set the longevity of videos.\n*The result is a bunch of videos with the certain longevity.\n*After 100MB worth of videos, they are being sent to user and later deleting.")

    async def send_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE, path: str):
        with open(path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    async def send_video_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        video_folder = app_config.AppConfig.VIDEO_FOLDER
        video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and f.lower().endswith(('.mp4', '.avi', '.mkv'))]

        for video_path in video_files:
            with open(video_path, 'rb') as video:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video)

    # errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')
