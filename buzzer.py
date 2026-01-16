#buzzer.py
from gpiozero import PWMOutputDevice
import time

# Cria PWM no GPIO17
bz = None
#PWMOutputDevice(17)

def init_buzzer():
    global bz
    if bz is None:
        try:
            bz = PWMOutputDevice(17)
        except Exception as e:
            print(f"[WARN] Buzzer not available: {e}")

def beep(duration=0.15, freq=4000):
    """
    Emite um beep de duração e frequência definidas.
    Frequência padrão: 2000 Hz.
    """
    try:
        bz.frequency = freq       # define frequência
        bz.value = 0.5            # 50% duty = som audível
        time.sleep(duration)
        bz.value = 0              # desliga o som
    except Exception as e:
        print("Buzzer error:", e)

def boot_beeps():
    pattern = [
        0.1, 0.1, 0.3,   # dois curtos + um longo
        0.1, 0.5        # curto + pausa maior
    ]

    for duration in pattern:
        beep()
        time.sleep(duration)

def tone(freq, duration):
    """
    Emite um tom contínuo com frequência específica.
    """
    try:
        bz.frequency = freq
        bz.value = 0.5
        time.sleep(duration)
        bz.value = 0
    except Exception as e:
        print("Tone error:", e)
