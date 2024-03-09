import OpenCV
from TelegramBot.bot import TelegramBot

class ApplicationManager:

    def launch_tgbot():
        bot = TelegramBot()
        bot.launch_bot()

    def start(cls):
        ApplicationManager.launch_tgbot()
        return

