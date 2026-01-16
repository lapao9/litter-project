# analyze_material.py

import os
import cv2
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import torch

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
# Load YOLOv5 Tiny
# =========================
# Usa modelo pré-treinado COCO, detecta objetos grandes (pode ajustar para dataset de lixo)
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
yolo_model.conf = 0.25  # confiança mínima
yolo_model.iou = 0.45   # IOU NMS

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
# Detect main object and apply background blur
# =========================
def isolate_main_object(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    results = yolo_model(img)
    detections = results.xyxy[0]  # [x1, y1, x2, y2, conf, class]

    if len(detections) == 0:
        # nenhum objeto detectado
        return img, None

    # pegar objeto com maior área
    areas = [(det[2]-det[0])*(det[3]-det[1]) for det in detections]
    max_idx = int(np.argmax(areas))
    x1, y1, x2, y2 = map(int, detections[max_idx][:4])

    # criar máscara
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255

    # desfocar fundo
    blurred = cv2.GaussianBlur(img, (21,21), 0)
    result = np.where(mask[:,:,None]==255, img, blurred)

    # retornar imagem com fundo desfocado e crop do objeto
    obj_crop = img[y1:y2, x1:x2].copy()
    return result, obj_crop

# =========================
# Main analyze function
# =========================
def analyze_material(image_path, confidence_threshold=0.1):
    if not os.path.exists(image_path):
        return "no_image"

    try:
        # Isola o objeto
        _, obj_img = isolate_main_object(image_path)
        if obj_img is None:
            # nenhum objeto detectado, usar imagem inteira
            img_for_model = cv2.imread(image_path)
        else:
            img_for_model = obj_img

        # Preprocessa
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
