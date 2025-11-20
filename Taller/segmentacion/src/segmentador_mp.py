import cv2
import numpy as np

class SimpleSegmenter:
    def __init__(self):
        pass

    def segment(self, frame, bbox):
        x1, y1, x2, y2 = map(int, bbox)

        # recorte del objeto detectado
        roi = frame[y1:y2, x1:x2]

        if roi.size == 0:
            return None

        # convertir a HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # segmentación simple por saturación
        _, s, _ = cv2.split(hsv)
        mask = cv2.threshold(s, 40, 255, cv2.THRESH_BINARY)[1]

        # redimensionar máscara a tamaño original
        full_mask = np.zeros(frame.shape[:2], dtype="uint8")
        full_mask[y1:y2, x1:x2] = mask

        return full_mask
