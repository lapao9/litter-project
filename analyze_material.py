import os
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "waste_classifier.tflite")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

with open(LABELS_PATH) as f:
    LABELS = [l.strip().lower() for l in f.readlines()]

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

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

H = input_details[0]["shape"][1]
W = input_details[0]["shape"][2]


def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (W, H))
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def blur_background(image_path, crop_fraction=0.5):
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    h, w = img.shape[:2]
    blurred = cv2.GaussianBlur(img, (21, 21), 0)

    ch, cw = int(h * crop_fraction), int(w * crop_fraction)
    y1, y2 = h // 2 - ch // 2, h // 2 + ch // 2
    x1, x2 = w // 2 - cw // 2, w // 2 + cw // 2

    blurred[y1:y2, x1:x2] = img[y1:y2, x1:x2]
    crop = img[y1:y2, x1:x2].copy()

    return blurred, crop


def analyze_material(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        return "no_image", None

    try:
        final_img, crop = blur_background(image_path)
        input_img = crop if crop is not None else cv2.imread(image_path)

        input_data = preprocess(input_img)
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()

        output = interpreter.get_tensor(output_details[0]["index"])[0]
        idx = int(np.argmax(output))
        confidence = float(output[idx])
        label = LABELS[idx]

        if confidence < confidence_threshold:
            return "unknown", final_img

        return CLASS_MAP.get(label, "other"), final_img

    except Exception as e:
        print("Analyze error:", e)
        return "error", None
