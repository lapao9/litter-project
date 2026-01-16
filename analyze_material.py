# analyze_material.py
import os
import cv2
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
# Preprocess image for TFLite
# =========================
def preprocess_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (INPUT_WIDTH, INPUT_HEIGHT))
    img = np.asarray(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# =========================
# Detect main object and blur background
# =========================
def isolate_main_object(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold automático baseado em Otsu
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        # Nenhum objeto detectado
        return img, None

    # Pegar maior contorno (assumimos objeto principal)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # Criar máscara
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[y:y+h, x:x+w] = 255

    # Desfocar fundo
    blurred = cv2.GaussianBlur(img, (21,21), 0)
    result = np.where(mask[:,:,None]==255, img, blurred)

    # Retornar crop do objeto
    obj_crop = img[y:y+h, x:x+w].copy()
    return result, obj_crop

# =========================
# Main analyze function
# =========================
def analyze_material(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        return "no_image"

    try:
        _, obj_img = isolate_main_object(image_path)
        if obj_img is None:
            # Nenhum objeto detectado, usar imagem inteira
            img_for_model = cv2.imread(image_path)
        else:
            img_for_model = obj_img

        # Preprocessar para TFLite
        input_data = preprocess_image(img_for_model)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Saída
        output_data = interpreter.get_tensor(output_details[0]['index'])[0]
        class_idx = int(np.argmax(output_data))
        confidence = float(output_data[class_idx])
        label = LABELS[class_idx]

        if confidence < confidence_threshold:
            return "unknown"

        return CLASS_MAP.get(label, "other")

    except Exception as e:
        print("Analyze error:", e)
        return "error"

# =========================
# Debug helper
# =========================
def debug_analyze(image_path):
    _, obj_img = isolate_main_object(image_path)
    if obj_img is None:
        img_for_model = cv2.imread(image_path)
    else:
        img_for_model = obj_img

    input_data = preprocess_image(img_for_model)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    print("\nPredictions:")
    for i, score in enumerate(output_data):
        print(f"{LABELS[i]:15s} -> {float(score):.3f}")
