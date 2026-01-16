# take_picture.py
import os
import time
import subprocess

OUTPUT_DIR = "output/frames"

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    print("Picamera2 not available, will use rpicam-still as fallback.")    

picam2 = None

def init_camera():
    """Initialize Picamera2 if available"""
    global picam2
    if not PICAMERA2_AVAILABLE:
        return False
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (1280, 720)})
        picam2.configure(config)
        picam2.start()
        time.sleep(0.5)
        return True
    except Exception as e:
        print("Error initializing Picamera2:", e)
        picam2 = None
        return False

def take_picture():
    """Take a picture and save to OUTPUT_DIR, return filepath or None on failure"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/frame_{int(time.time())}.jpg"

    # 1️⃣ Tentar Picamera2
    if PICAMERA2_AVAILABLE and picam2 is not None:
        try:
            picam2.capture_file(filename)
            return filename
        except Exception as e:
            print("Picamera2 capture failed:", e)

    # 2️⃣ Fallback para rpicam-still (SSH-friendly)
    try:
        cmd = ["rpicam-still", "-n", "--output", filename]
        subprocess.run(cmd, check=True)
        return filename
    except Exception as e:
        print("rpicam-still failed:", e)
        return None

def close_camera():
    """Close Picamera2 if initialized"""
    global picam2
    if picam2 is not None:
        picam2.stop()
        picam2.close()
        picam2 = None

# Initialize camera at startup
init_camera()
