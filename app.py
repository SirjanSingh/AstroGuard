import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2

# Load the YOLOv8 model
model = YOLO('best.pt')

# Streamlit UI
st.set_page_config(page_title="AstroGuard 🚀", layout="centered")
st.title("🛰️ AstroGuard: Space Station Object Detector")
st.markdown("Upload an image and we'll detect Fire Extinguisher, ToolBox, or OxygenTank using our AI model.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Perform prediction
    results = model.predict(temp_path, conf=0.5)_
