import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

pwm = GPIO.PWM(17, 4000)  # 2000 Hz = 2 kHz
pwm.start(50)             # 50% duty cycle

time.sleep(3)
pwm.stop()
GPIO.cleanup()
