import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

print("Ligando GPIO17…")
GPIO.output(17, GPIO.HIGH)
time.sleep(1)

print("Estado esperado: HIGH")
print("Desligando GPIO17…")
GPIO.output(17, GPIO.LOW)
time.sleep(1)

print("Estado esperado: LOW")

GPIO.cleanup()
