import streamlit as st
import cv2
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.camera_thread import CameraThread

st.title("Detección + Segmentación Simplificada (YOLO)")

# Iniciar cámara
cam = st.session_state.get("cam", None)
if cam is None:
    cam = CameraThread()
    cam.start()
    st.session_state["cam"] = cam

stframe = st.empty()
stmask = st.empty()
stdets = st.empty()

while True:
    results = cam.get()
    frame = results["frame"]
    mask = results["mask"]
    detections = results["detections"]

    if frame is None:
        continue

    # Convertir frame a RGB para Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    stframe.image(frame_rgb, caption="Cámara en tiempo real")

    if mask is not None:
        stmask.image(mask, caption="Segmentación (máscara generada)")

    stdets.write(detections)

