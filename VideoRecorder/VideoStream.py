import cv2 
import threading 


class StreamHandler(threading.Thread):
    def __init__(self, camera_id, w = 640, h = 480, fps = 30):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id)
        self.configure_camera(w,h,fps)

    def configure_camera(self, w, h, fps):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

    def get_frame(self):
        
        # print(f'######### Active Thread Count: {threading.active_count()} #########')
        ret, frame = self.cap.read()
        return frame if ret else None
    

