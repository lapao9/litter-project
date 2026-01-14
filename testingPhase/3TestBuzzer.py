from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(17, frequency=4000, initial_value=0.5)

sleep(3)
buzzer.off()
