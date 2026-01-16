# main.py
import os
import json
import time
import signal
import sys
from datetime import datetime
from gpiozero import Button
import cv2

from local_server import run_in_thread as start_http_server
from take_picture import take_picture
from analyze_material import analyze_material
from buzzer import beep, boot_beeps, init_buzzer
from send_to_db import send_detection_to_db
from location import get_location
from device_id import get_stick_id


# =========================
# INIT
# =========================
init_buzzer()

BUTTON_GPIO = 20
OUTPUT_JSON_DIR = "output/detections"
BASE_FRAMES_DIR = "output/frames"

os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
os.makedirs(BASE_FRAMES_DIR, exist_ok=True)

# 🔹 CURRENT SESSION
SESSION_ID = int(time.time())
SESSION_DIR = os.path.join(BASE_FRAMES_DIR, f"session_{SESSION_ID}")
os.makedirs(SESSION_DIR, exist_ok=True)

button = Button(BUTTON_GPIO, bounce_time=0.1)


def get_rpi_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


BASE_IMAGE_URL = f"http://{get_rpi_ip()}:8000/output/frames/session_{SESSION_ID}"


# =========================
# EXIT HANDLER
# =========================
def graceful_exit(signum, frame):
    print("\nGraceful exit requested. Bye.")
    sys.exit(0)


signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)


# =========================
# PRINT RESULT
# =========================
def print_detection(material, filename, db_id, image_url):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 50)
    print(f"[{now}] Detection Result")
    print(f"Material : {material}")
    print(f"DB ID    : {db_id if db_id else 'N/A'}")
    print(f"Image    : {image_url}")
    print("=" * 50 + "\n")


# =========================
# MAIN PROCESS
# =========================
def process_once():
    print("📸 Taking picture...")
    image_path = take_picture()

    if image_path is None:
        print("❌ Capture failed")
        return

    print("🧠 Analyzing material...")
    material, final_image = analyze_material(image_path)

    filename = os.path.basename(image_path)

    # 🔹 Save
    save_path = os.path.join(SESSION_DIR, filename)
    image_url = f"{BASE_IMAGE_URL}/{filename}"

    # Save blurred image
    if final_image is not None:
        cv2.imwrite(save_path, final_image)
    else:
        cv2.imwrite(save_path, cv2.imread(image_path))

    beep()

    # Save JSON 
    timestamp = int(time.time())
    json_path = os.path.join(OUTPUT_JSON_DIR, f"det_{timestamp}.json")

    with open(json_path, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "image": filename,
            "image_url": image_url,
            "material": material,
            "session": SESSION_ID
        }, f, indent=2)

    # Location + device
    lat, lon = get_location()
    stick_id = get_stick_id()

    # DB material mapping
    db_material = material #if material in [
    #    "plastic", "metal", "paper", "glass", "organic", "other"
    #] else "other"

    # Send to DB
    db_id = None
    try:
        db_ok = send_detection_to_db(
            material=db_material,
            description=f"Detected material: {material}",
            image_url=image_url,
            latitude=lat,
            longitude=lon,
            stick_id=stick_id
        )
        if db_ok:
            db_id = db_ok
            print("✅ Saved to DB")
        else:
            print("❌ DB insert failed")
    except Exception as e:
        print("❌ DB ERROR:", e)

    print_detection(material, filename, db_id, image_url)


# =========================
# MAIN LOOP
# =========================
def main():
    print("🌍 Starting HTTP server...")
    start_http_server()

    boot_beeps()
    print("✅ System ready – press the button")

    while True:
        button.wait_for_press()
        print("🔘 Button pressed")
        process_once()
        time.sleep(0.7)


if __name__ == "__main__":
    main()
