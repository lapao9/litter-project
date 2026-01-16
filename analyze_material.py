# analyze_material.py

import os
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite


# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "model", "waste_classifier.tflite")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")


# =========================
# Load labels
# =========================
with open(LABELS_PATH, "r") as f:
    LABELS = [line.strip().lower() for line in f.readlines()]


# =========================
# Class mapping (robust)
# =========================
CLASS_MAP = {
    "battery": "battery",
    "biological": "organic",

    "brown-glass": "glass",
    "green-glass": "glass",
    "white-glass": "glass",

    "metal": "metal",
    "paper": "paper",
    "cardboard": "cardboard",
    "plastic": "plastic",

    "clothes": "textile",
    "shoes": "textile",

    "trash": "trash"
}


# =========================
# Load TFLite model
# =========================
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH  = input_details[0]["shape"][2]


# =========================
# Image preprocessing
# =========================
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((INPUT_WIDTH, INPUT_HEIGHT))
    img = np.asarray(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# =========================
# Main inference function
# =========================
def analyze_material(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        return "no_image"

    try:
        # Prepare input
        input_data = preprocess_image(image_path)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        # Get output
        output_data = interpreter.get_tensor(output_details[0]["index"])[0]

        # Top prediction
        class_idx = int(np.argmax(output_data))
        confidence = float(output_data[class_idx])
        label = LABELS[class_idx]

        # Reject low confidence
        if confidence < confidence_threshold:
            return "unknown (confidence to low)"
        print(confidence)

        # Map to system category
        return CLASS_MAP.get(label, "other")

    except Exception as e:
        print("Analyze error:", e)
        return "error"


# =========================
# Debug helper (optional)
# =========================
def debug_analyze(image_path):
    input_data = preprocess_image(image_path)
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])[0]

    print("\nPredictions:")
    for i, score in enumerate(output_data):
        print(f"{LABELS[i]:15s} -> {float(score):.3f}")
