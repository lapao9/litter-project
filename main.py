import json
import time
import os
import signal
import sys
from gpiozero import Button
from datetime import datetime

from local_server import run_in_thread as start_http_server
from take_picture import take_picture
from analyze_material import analyze_material
from buzzer import beep
from buzzer import init_buzzer
from send_to_db import send_detection_to_db
from location import get_location
from device_id import get_stick_id

init_buzzer()

# ------------------ CONFIG ------------------
BUTTON_GPIO = 20
OUTPUT_JSON_DIR = "output/detections"
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

def get_rpi_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

BASE_IMAGE_URL = f"http://{get_rpi_ip()}:8000/output/frames"

button = Button(BUTTON_GPIO, bounce_time=0.1)

# ------------------ EXIT HANDLER ------------------
def graceful_exit(signum, frame):
    print("\nGraceful exit requested. Bye.")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# ------------------ DETECTION PRINT ------------------
def print_detection(material, json_file, image_file, db_id, base_url=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = base_url
    print("\n" + "="*50)
    print(f"[{now}] Detection Result:")
    print(f"Detected Material : {material}")
    print(f"Saved to DB with ID: {db_id if db_id else 'N/A'}")
    print(f"URL              : {url}")
    print("="*50 + "\n")

# ------------------ PROCESS ------------------
def process_once():
    print("Taking picture...")
    image_path = take_picture()

    if image_path is None:
        print("Capture failed — skipping analyze.")
        material_detected = "no_image"
        material_db = "other"   # DB não aceita "no_image"
        filename = "no_image.jpg"
        imageUrl = ""
    else:
        print("Analyzing Material...")
        material_detected = analyze_material(image_path)
        material_db = material_detected if material_detected in ["plastic", "metal", "paper", "glass", "organic", "other"] else "other"
        filename = os.path.basename(image_path)
        imageUrl = f"{BASE_IMAGE_URL}/{filename}"

    beep()

    # Save JSON
    timestamp = int(time.time())
    json_path = os.path.join(OUTPUT_JSON_DIR, f"det_{timestamp}.json")
    result = {
        "timestamp": timestamp,
        "image": image_path if image_path else "",
        "image_url": imageUrl,
        "material": material_detected
    }
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    print("Detected material:", material_detected)
    print("Saved JSON:", json_path)
    print("Image filename:", filename)

    # Location & device
    lat, lon = get_location()
    stick_id = get_stick_id()

    # Send to DB
    db_id = None
    try:
        db_ok = send_detection_to_db(
            material=material_db,
            description=f"Detected material: {material_detected}",
            image_url=imageUrl,
            latitude=lat,
            longitude=lon,
            stick_id=stick_id
        )
        if db_ok:
            db_id = db_ok  # assume que retorna ID
            print("Saved to DB ✅")
        else:
            print("Failed to save to DB ❌")
    except Exception as e:
        print("DB ERROR:", e)

    # Print full detection info
    base_url = imageUrl
    print_detection(material_detected, json_path, filename, db_id, base_url=base_url)

# ------------------ MAIN ------------------
def main():
    print("Starting HTTP server...")
    start_http_server()

    print("System ready. Press button to scan (CTRL+C to stop).")

    while True:
        button.wait_for_press()
        print("Button pressed!")
        process_once()
        time.sleep(0.7)

if __name__ == "__main__":
    main()
