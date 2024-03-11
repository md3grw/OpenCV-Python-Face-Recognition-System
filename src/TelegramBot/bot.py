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
        await update.message.reply_text("Test")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Test")

    async def send_video_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        video_folder = app_config.AppConfig.VIDEO_FOLDER

        # Get a list of all files in the video folder
        video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]

        for video_file in video_files:
            video_path = os.path.join(video_folder, video_file)

            # Check if the file is a video (you might want to improve this check)
            if video_file.endswith(('.mp4', '.avi', '.mkv')):
                await update.message.reply_video(video_path)

    # errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')
