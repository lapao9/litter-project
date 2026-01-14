from gpiozero import Buzzer
import time

b = Buzzer(17)
print('Beep in 1s')
time.sleep(1)
b.on()
time.sleep(0.2)
b.off()
