import threading
import numpy as np
from src.detector_yolo import YOLODetector

class Pipeline:
    def __init__(self):
        self.detector = YOLODetector()

        self.lock = threading.Lock()
        self.results = {
            "frame": None,
            "detections": [],
            "mask": None
        }

    def process_frame(self, frame):
        detecciones = self.detector.detect(frame)

        # --------------------------------------------
        # Crear "segmentación" basada en los bounding boxes
        # --------------------------------------------
        mask = np.zeros(frame.shape[:2], dtype="uint8")

        for det in detecciones:
            x1, y1, x2, y2 = map(int, det["bbox"])
            mask[y1:y2, x1:x2] = 255  # color blanco donde hay objeto

        # Guardar resultados
        with self.lock:
            self.results["frame"] = frame
            self.results["detections"] = detecciones
            self.results["mask"] = mask

    def get_results(self):
        with self.lock:
            return self.results.copy()

