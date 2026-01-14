from picamera2 import Picamera2
import time

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1280,720)})
picam2.configure(config)
picam2.start()
time.sleep(0.5)
picam2.capture_file("test_python.jpg")
picam2.stop()
picam2.close()
print("Foto tirada com sucesso!")
