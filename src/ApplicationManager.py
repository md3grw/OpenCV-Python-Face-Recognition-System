import OpenCV

class ApplicationManager:
    def Start():
        #add: create "remote control" for the camera, u could enable face recognition in the TG bot
        OpenCV.process_data() #launch the process
        OpenCV.video_capture.release()
        OpenCV.cv2.destroyAllWindows()
        return
    
