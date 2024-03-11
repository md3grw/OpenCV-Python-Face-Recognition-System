import cv2
import time
import os
import app_config

class OpenCV:
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    video_capture = cv2.VideoCapture(0)

    @staticmethod
    def detect_bounding_box(vid):
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = OpenCV.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        return faces

    @staticmethod
    def record_video(exit_flag):
        video_codec = cv2.VideoWriter_fourcc(*'mp4v')
        recording_duration = 15  # seconds
        frames_per_second = 24.0
        output_dir = os.path.expanduser(app_config.AppConfig.VIDEO_FOLDER)
        os.makedirs(output_dir, exist_ok=True)

        while not exit_flag.is_set():
            current_time = time.strftime('%Y-%m-%d_%H-%M-%S')
            output_path = os.path.join(output_dir, f'recording_{current_time}.mp4')
            resolution = (int(OpenCV.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                          int(OpenCV.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            video_writer = cv2.VideoWriter(output_path, video_codec, frames_per_second, resolution)

            start_time = time.time()
            while time.time() - start_time < recording_duration:
                result, video_frame = OpenCV.video_capture.read()
                if not result:
                    break
                faces = OpenCV.detect_bounding_box(video_frame)
                video_writer.write(video_frame)

            video_writer.release()
            print(f"Video saved: {output_path}")
            time.sleep(1)  # Wait for 1 second before starting the next recording

        OpenCV.video_capture.release()