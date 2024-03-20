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

        # Create thread for the camera
        camera_thread = threading.Thread(target=cls.launch_camera, args=(exit_flag,))

        try:
            # Start the camera thread
            camera_thread.start()

            # Run the Telegram Bot in the main thread
            cls.launch_tgbot()

        except KeyboardInterrupt:
            exit_flag.set()  # Set the exit flag to stop the camera processing loop

        finally:
            # Wait for the camera thread to finish
            camera_thread.join()