#take_picture.py
from picamera2 import Picamera2
import os
import time

OUTPUT_DIR = "output/frames"

def take_picture():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/frame_{int(time.time())}.jpg"

    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (1280, 720)}
        )
        picam2.configure(config)
        picam2.start()
        time.sleep(0.6)
        picam2.capture_file(filename)
        picam2.stop()
        picam2.close()
        return filename
    except Exception as e:
        print("Camera error:", e)
        return None

