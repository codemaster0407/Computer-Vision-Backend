from fastapi import FastAPI
from fastapi.responses import Response, StreamingResponse
import cv2
import uvicorn
from VideoStream import StreamHandler 
from ClientHandler import ClientHandler
import threading 
from Config import *



app = FastAPI()

# global videoStream
videoStream = StreamHandler(0, w = 640, h = 480, fps = 30)



def return_feed():
    while True:
        frame = videoStream.get_frame()
        if frame is not None :
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame as a chunk of bytes
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            raise Exception('Stream is Not read. Check Camera Configuration')
        
@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(return_feed(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.post('/start_recording')
async def start_recording(client_id: str):
    client = ClientHandler(client_id, videoStream, w = 640, h = 480, fps = 30)
    client_thread = threading.Thread(target=client.record_video)
    
    client_users[client_id] = {'client_obj': client, 
                               'client_thread': client_thread
                               }
    client_thread.start()
    
    
    return {'status:': 'Recording Started'}, 200

@app.post('/pause_recording')
def pause_recording(client_id: str):
    # global client
    client = client_users[client_id]['client_obj'] 
    client.pause_recording()
    return {'status:': 'Recording Paused'} , 200

@app.post('/resume_recording')
def resume_recording(client_id: str):
    # global client
    client = client_users[client_id]['client_obj']
    client.resume_recording()
    return {'status':'Resume Recording'}, 200



@app.post('/stop_recording')
def stop_recording(client_id: str):
    
    client =  client_users[client_id]['client_obj']
    client.save_recording()
    client_users[client_id]['client_thread'].join()

    try:
        del client_users[client_id]
    except KeyError:
        return {'status': 'Client still hasn\'t started recording'} , 400
    return {'status': 'Recording Saved'}, 200
@app.get("/")
async def root():
    return {"message": "Welcome to the video feed server!"}

@app.get("/health")
async def get_health():
    if threading.active_count() > 20:
        return {'message': 'Server is very occupied'}, 200
    else:
        return {'message' : 'Server is healthy'} , 200
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)