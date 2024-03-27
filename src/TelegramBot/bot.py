from telegram import Update
from TelegramBot import handlers
from TelegramBot import config
import app_config
import os
import OpenCV
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from logger import Logger 

VIDEO_LENGTH = 15

class TelegramBot:
    def __init__(self):
        self.TOKEN = config.Config.TELEGRAM_BOT_TOKEN


    def launch_bot(self):
        Logger.log('info', 'TelegramBot got launched')
        app = Application.builder().token(self.TOKEN).build()

        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("send_media", self.send_media_command))
        app.add_handler(CommandHandler("send_video", self.send_video_command))
        app.add_handler(CommandHandler("send_photos", self.send_photos_command))
        app.add_handler(CommandHandler("add_face", self.add_face_command))
        app.add_handler(CommandHandler("delete_photos", self.delete_photos))
        app.add_handler(CommandHandler("delete_videos", self.delete_videos))
        app.add_handler(CommandHandler("delete_media", self.delete_media))
        app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT, self.handle_add_face))

        app.add_error_handler(self.error)
        app.run_polling(poll_interval=3)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/start command')
        await update.message.reply_text(
            "Hello there! 👋 Welcome to SpectatorBot! I'm here to assist you with operating your video camera." +
            "\nhttps://github.com/md3grw/OpenCV-Python-Face-Recognition-System" + 
            "\nTo get started, feel free to explore the available commands. If you ever need help, just type /help. Enjoy your time with SpectatorBot!")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/help command')
        await update.message.reply_text(
            "The bot records video and detects faces, user can control it through Telegram bot, recognizes faces(you need to train the model)." +
            "\nType /add_face to add new trusted face."
            "\nType /send_video to get the videos." + 
            "\nType /send_photos to get all of the photos" + 
            "\nType /send_media to get photos, videos and logs" + 
            "\nType /delete_media to delete photos, videos" + 
            "\nType /delete_photos to delete photos" + 
            "\nType /delete_videos to delete videos" + 
            "\n*As a result you are getting videos with N length, photos and logs about movement/faces appeared.")
            

    async def send_photos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/send_photos command')
        photo_folder = app_config.AppConfig.PHOTO_FOLDER
        photo_files = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(photo_folder, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        for photo_path in photo_files:
            with open(photo_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)


    async def setup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Logger.log('info', '/setup command')
        await update.message.reply_text("Let's set up the video parameters.")
        await update.message.reply_text("How long do you want the videos to be (in seconds)?")
        return VIDEO_LENGTH

    async def add_face_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Logger.log('info', '/add_face command')
        await update.message.reply_text("Please send a picture of the person's face.")
        context.user_data["add_face_state"] = "photo"

    async def delete_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/delete_photos command')
        photo_folder = app_config.AppConfig.PHOTO_FOLDER
        photo_files = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(photo_folder, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
        for photo_path in photo_files:
            os.remove(photo_path)
            Logger.log('info', f'Deleted video: {photo_path}')
        
        await update.message.reply_text("All photos have been deleted.")
        
    async def delete_videos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/delete_videos command')
        video_folder = app_config.AppConfig.VIDEO_FOLDER
        video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and f.lower().endswith(('.mp4', '.avi', '.mkv'))]
    
        for video_path in video_files:
            os.remove(video_path)
            Logger.log('info', f'Deleted video: {video_path}')
        
        await update.message.reply_text("All videos have been deleted.")
    
    async def delete_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/delete_media command')
        await self.delete_photos(update, context)
        await self.delete_media(update, context)

    async def handle_add_face(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        state = context.user_data.get("add_face_state")
        if state == "photo":
            photo_file = update.message.photo[-1].file_id
            photo_path = f"{app_config.AppConfig.KNOWN_FACES_FOLDER}/{update.message.chat_id}.jpg"
            file = await context.bot.get_file(photo_file)
            file_bytes = await file.download_as_bytearray()
            with open(photo_path, 'wb') as photo_local:
                photo_local.write(file_bytes)
            await update.message.reply_text("Please enter the name of the person.")
            context.user_data["photo_path"] = photo_path
            context.user_data["add_face_state"] = "name"
        elif state == "name":
            name = update.message.text
            photo_path = context.user_data["photo_path"]
            #OpenCV.OpenCV.add_face(photo_path, name)
            #you have to train opencv to use recognizer
            await update.message.reply_text(f"Successfully added {name}'s face.")
            context.user_data.pop("add_face_state", None)
            context.user_data.pop("photo_path", None)

    async def send_media_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/send_media command')
        await self.send_photos_command(update, context)
        await self.send_video_command(update, context)
        with open(app_config.AppConfig.LOG_PATH, "rb") as logs:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=logs)

    async def send_video_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        Logger.log('info', '/send_video command')
        video_folder = app_config.AppConfig.VIDEO_FOLDER
        video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and f.lower().endswith(('.mp4', '.avi', '.mkv'))]
        for video_path in video_files:
            with open(video_path, 'rb') as video:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video)

    # errors
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')