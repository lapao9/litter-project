# device_id.py
import os
import pathlib

STICK_ID_FILE = "/home/pi/.stick_id"  # local seguro para guardar ID persistente


def get_rpi_serial():
    """Get the Raspberry Pi serial number from /proc/cpuinfo."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    return line.split(":")[1].strip()
    except Exception:
        return None


def generate_numeric_id(serial: str) -> int:
    """
    Converts a hex serial string to a numeric ID.
    """
    return int(serial[-8:], 16)   # últimos 8 dígitos do serial → inteiro


def get_stick_id():
    """
    Returns a persistent numeric ID for the device.
    - First checks if ID file exists
    - If not, gets RPi serial
    - Then saves and uses it always
    """
    #1. verify if ID file exists
    if os.path.exists(STICK_ID_FILE):
        try:
            with open(STICK_ID_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass  

    # 2. Get RPi serial
    serial = get_rpi_serial()
    if serial is None:
        # Fallback serial if not available
        serial = "0000000000000000"

    # 3. Convert to numeric ID
    stick_id = generate_numeric_id(serial)

    # 4. Save to file for future use
    try:
        with open(STICK_ID_FILE, "w") as f:
            f.write(str(stick_id))
    except:
        pass  

    return stick_id
