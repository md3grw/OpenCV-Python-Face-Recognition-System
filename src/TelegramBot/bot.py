from telegram import Update
from TelegramBot import handlers
from TelegramBot import config
import app_config
import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

SETUP, VIDEO_LENGTH, NOTIFICATION_FREQUENCY, SEND_PHOTOS = range(4)

class TelegramBot:
    def __init__(self):
        self.TOKEN = config.Config.TELEGRAM_BOT_TOKEN

    def launch_bot(self):
        app = Application.builder().token(self.TOKEN).build()
        bot_instance = self  # Create an instance of TelegramBot

        setup_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("setup", bot_instance.setup_command)],
            states={
                VIDEO_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_instance.video_length)],
                NOTIFICATION_FREQUENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_instance.notification_frequency)],
            },
            fallbacks=[],
        )

        app.add_handler(setup_conv_handler)
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("send_video", self.send_video_command))
        app.add_handler(CommandHandler("send_photos", self.send_photos_command))
        app.add_handler(MessageHandler(filters.TEXT, handlers.handle_message))
        app.add_error_handler(self.error)
        app.run_polling(poll_interval=3)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Hello there! 👋 Welcome to SpectatorBot! I'm here to assist you with operating your video camera." +
            "\nhttps://github.com/md3grw/OpenCV-Python-Face-Recognition-System" + 
            "\nTo get started, feel free to explore the available commands. If you ever need help, just type /help. Enjoy your time with SpectatorBot!")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "The bot records video and detects faces, notifies user every N amount of time about what happened, recognizes faces." +
            "\nType /add_face to add new trusted face."
            "\nType /send_video to get the videos." + 
            "\nType /send_photos to get all of the photos" + 
            "\nType /setup to set up longevity of the videos, how often do you want to get notified, etc." + 
            "\n*As a result you are getting videos with N length, photos and logs about movement/faces appeared." + 
            "\n*After 100MB worth of videos, they are being sent to user and later deleting." + 
            "\n*Same with photos.")
            

    async def send_photos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, path: str):
        photo_folder = app_config.AppConfig.PHOTO_FOLDER
        photo_files = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(photo_folder, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        for photo_path in photo_files:
            with open(photo_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)


    async def setup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text("Let's set up the video parameters.")
        await update.message.reply_text("How long do you want the videos to be (in seconds)?")
        return VIDEO_LENGTH

    async def video_length(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            video_duration = int(update.message.text)
            context.user_data["video_duration"] = video_duration
            await update.message.reply_text(f"Video duration set to {video_duration} seconds.")
            await update.message.reply_text("How often do you want to be notified about motion (in minutes)?")
            return NOTIFICATION_FREQUENCY
        except ValueError:
            await update.message.reply_text("Invalid input. Please enter a number.")
            return VIDEO_LENGTH

    async def notification_frequency(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            notification_frequency = int(update.message.text)
            context.user_data["notification_frequency"] = notification_frequency
            await update.message.reply_text(f"Notification frequency set to {notification_frequency} minutes.")
            # You can add more prompts here or end the conversation
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("Invalid input. Please enter a number.")
            return NOTIFICATION_FREQUENCY

    async def send_video_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        video_folder = app_config.AppConfig.VIDEO_FOLDER
        video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and f.lower().endswith(('.mp4', '.avi', '.mkv'))]
        for video_path in video_files:
            with open(video_path, 'rb') as video:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video)

    # errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')