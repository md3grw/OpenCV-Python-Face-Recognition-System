import cv2
import time
import os
import app_config

class OpenCV:
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    video_capture = cv2.VideoCapture(0)

    video_capture = cv2.VideoCapture(0)
    previous_frame = None
    
    @staticmethod
    def detect_bounding_box(vid):
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = OpenCV.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        return faces

    @staticmethod
    def capture_photo():
        output_dir = os.path.expanduser(app_config.AppConfig.PHOTO_FOLDER)
        os.makedirs(output_dir, exist_ok=True)

        current_time = time.strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(output_dir, f'photo_{current_time}.jpg')

        result, frame = OpenCV.video_capture.read()
        if result:
            cv2.imwrite(output_path, frame)
            print(f"Photo saved: {output_path}")
            return output_path
        else:
            print("Failed to capture photo.")

    def detect_motion(self, frame):
        motion_detected = False
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)

        if self.previous_frame is None:
            self.previous_frame = gray_frame
            return motion_detected, frame  # Return None for threshold

        frame_delta = cv2.absdiff(self.previous_frame, gray_frame)
        threshold = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)

        contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.previous_frame = gray_frame  # Update previous_frame here

        return motion_detected, frame

    def record_video(self, exit_flag):
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

                motion_detected, motion_frame = self.detect_motion(video_frame)

                faces = OpenCV.detect_bounding_box(video_frame)

                print(f"Motion detected status: {motion_detected}")

                if motion_detected:
                    #photo_path = OpenCV.capture_photo()
                    
                    if len(faces) > 0:
                        print("Face and motion detected!")
                    else:
                        print("Motion detected!")

                video_writer.write(video_frame)

            video_writer.release()
            print(f"Video saved: {output_path}")
            time.sleep(1) 

        OpenCV.video_capture.release()