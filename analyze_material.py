#analyze_material.py
import numpy as np
from PIL import Image
#import tflite_runtime.interpreter as tflite
import tensorflow as tf
import os

tflite = tf.lite

MODEL_PATH = "model/waste_classifier.tflite"
LABELS_PATH = "model/labels.txt"

# carregar labels
with open(LABELS_PATH, "r") as f:
    LABELS = [line.strip() for line in f.readlines()]

# carregar modelo
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

INPUT_HEIGHT = input_details[0]["shape"][1]
INPUT_WIDTH = input_details[0]["shape"][2]

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((INPUT_WIDTH, INPUT_HEIGHT))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def analyze_material(image_path):
    if not os.path.exists(image_path):
        return "no_image"

    try:
        input_data = preprocess_image(image_path)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])[0]
        class_idx = int(np.argmax(output_data))
        label = LABELS[class_idx].lower()

        # mapear para categorias do teu sistema
        if label in ["plastic", "metal", "paper", "glass"]:
            return label
        elif label == "cardboard":
            return "paper"
        elif label == "trash":
            return "other"
        else:
            return "organic"

    except Exception as e:
        print("Analyze error:", e)
        return "error"
