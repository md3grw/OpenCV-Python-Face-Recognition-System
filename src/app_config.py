import os

class AppConfig:
    username = os.getlogin()
    BASE_DIR = "/Users" if os.name == "posix" else "C:\\Users"  # macOS vs Windows
    LOG_PATH = os.path.join(BASE_DIR, username, "documents", "facedetect_data", "logger.log")
    VIDEO_FOLDER = os.path.join(BASE_DIR, username, "documents", "replays")
    KNOWN_FACES_FOLDER = os.path.join(BASE_DIR, username, "documents", 'facedetect_knownfaces')
    PHOTO_FOLDER = os.path.join(BASE_DIR, username, "documents", "facedetect_photos")

        
os.makedirs('/Users/egormoskalenko/documents/facedetect_data/', exist_ok=True)
os.makedirs(AppConfig.VIDEO_FOLDER, exist_ok=True)
os.makedirs(AppConfig.KNOWN_FACES_FOLDER, exist_ok=True)
os.makedirs(AppConfig.PHOTO_FOLDER, exist_ok=True)
