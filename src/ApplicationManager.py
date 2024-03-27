import threading
import queue
from OpenCV import OpenCV
from TelegramBot.bot import TelegramBot

class ApplicationManager:
    @staticmethod
    def launch_camera(exit_flag):
        opencv = OpenCV()
        opencv.record_video(exit_flag)

    @staticmethod
    def launch_tgbot():
        bot = TelegramBot()
        bot.launch_bot()

    @classmethod
    def start(cls):
        exit_flag = threading.Event()

        camera_thread = threading.Thread(target=cls.launch_camera, args=(exit_flag,))

        try:
            camera_thread.start()

            cls.launch_tgbot()

        except KeyboardInterrupt:
            exit_flag.set()  # Set the exit flag to stop the camera processing loop

        finally:
            camera_thread.join()