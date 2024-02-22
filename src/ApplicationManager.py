from OpenCV import OpenCV

class ApplicationManager:
    @classmethod
    def start(cls):

        obj = OpenCV()

        #add: create "remote control" for the camera, u could enable face recognition in the TG bot
        obj.process_data() #launch the process
        obj.video_capture.release()
        obj.cv2.destroyAllWindows()
        return
    
