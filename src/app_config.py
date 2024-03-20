import os

class AppConfig:
    username = os.getlogin()
    VIDEO_FOLDER = "/Users/"+username+"/documents/replays"
    PHOTO_FOLDER = "/Users/"+username+"/documents/facedetect_photos"