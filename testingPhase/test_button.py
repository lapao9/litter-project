import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from datetime import datetime

# Configuração GPIO
BUTTON_PIN = 20
BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Inicializa câmera
picam2 = Picamera2()
picam2.start()

try:
    print("Sistema pronto. Pressione o botão...")
    while True:
        if GPIO.input(BUTTON_PIN) == 0:  # botão pressionado
            print("Botão pressionado!")
            
            # Toca buzzer
            GPIO.output(BUZZER_PIN, 1)
            time.sleep(0.5)
            GPIO.output(BUZZER_PIN, 0)
            
            # Criar nome de arquivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/home/pi/litter_project/images_ai/foto_{timestamp}.jpg"
            
            # Tirar foto
            picam2.capture_file(filename)
            print(f"Foto salva em {filename}")
            
            # Aguarda soltar botão (evita múltiplas fotos por clique)
            while GPIO.input(BUTTON_PIN) == 0:
                time.sleep(0.1)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Encerrando...")
finally:
    GPIO.cleanup()
