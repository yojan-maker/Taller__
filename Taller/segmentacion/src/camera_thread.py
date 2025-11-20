  GNU nano 7.2                                                                                                    camera_thread.py                                                                                                              
import threading
import cv2
from src.pipeline import Pipeline

class CameraThread(threading.Thread):
    def __init__(self, src=0):
        super().__init__()
        self.capture = cv2.VideoCapture(src)
        self.pipeline = Pipeline()
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            self.pipeline.process_frame(frame)

    def get(self):
        return self.pipeline.get_results()

    def stop(self):
        self.running = False
        self.capture.release()







