import json
import time
import os
import signal
import sys
from gpiozero import Button

from local_server import run_in_thread as start_http_server
from take_picture import take_picture
from analyze_material import analyze_material
from buzzer import beep
from send_to_db import send_detection_to_db
from location import get_location
from device_id import get_stick_id

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

def graceful_exit(signum, frame):
    print("\nGraceful exit requested. Bye.")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

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

        # fallback seguro para DB
        if material_detected not in ["plastic", "metal", "paper", "glass", "organic", "other"]:
            material_db = "other"
        else:
            material_db = material_detected

        filename = os.path.basename(image_path)
        imageUrl = f"{BASE_IMAGE_URL}/{filename}"

    print("Detected material:", material_detected)  # mostra sempre o que o modelo retornou

    # Beep sempre
    beep()

    # Save detection JSON
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

    print("Saved JSON:", json_path)
    print("Image filename:", filename)

    # Get geolocation
    lat, lon = get_location()

    # Get stick Id
    stick_id = get_stick_id()

    # Send to database
    try:
        db_ok = send_detection_to_db(
            material=material_db,  # envia valor seguro
            description=f"Detected material: {material_detected}",  # mantém o nome real
            image_url=imageUrl,
            latitude=lat,
            longitude=lon,
            stick_id=stick_id
        )
        if db_ok:
            print("Saved to DB ✅")
        else:
            print("Failed to save to DB ❌")
    except Exception as e:
        print("DB ERROR:", e)


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
