import cv2 
import os 
import threading 



class ClientHandler:
    def __init__(self, client_id,videoStream,  w, h , fps):
        self.out = cv2.VideoWriter(f"Recordings/{client_id}.mp4", cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
        self.RECORD_FLAG = True 
        self.client_id = client_id 
        self.videoStream = videoStream
        print(type(self.out))

    def pause_recording(self):
        self.RECORD_FLAG = False
    def resume_recording(self):
        self.RECORD_FLAG = True

    def record_video(self):
        while self.RECORD_FLAG:
            frame = self.videoStream.get_frame()
            self.out.write(frame)
            # print(frame.shape)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    def save_recording(self):
        self.RECORD_FLAG = False
        self.out.release()


    

