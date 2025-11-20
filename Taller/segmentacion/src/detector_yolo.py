from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, weights_path="model/best.pt"):
        self.model = YOLO(weights_path)

    def detect(self, frame):
        results = self.model(frame)[0]

        detecciones = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            score = float(box.conf[0])
            label = self.model.names[cls]

            detecciones.append({
                "label": label,
                "score": score,
                "bbox": [x1, y1, x2, y2],
            })
        return detecciones







