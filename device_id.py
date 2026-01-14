# device_id.py
import os
import pathlib

STICK_ID_FILE = "/home/pi/.stick_id"  # local seguro para guardar ID persistente


def get_rpi_serial():
    """Obtém o número de série REAL da Raspberry Pi."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    return line.split(":")[1].strip()
    except Exception:
        return None


def generate_numeric_id(serial: str) -> int:
    """
    Converte o serial hex da Raspberry Pi num número inteiro estável.
    É curto, fácil de ler, mas sempre igual.
    """
    return int(serial[-8:], 16)   # últimos 8 dígitos do serial → inteiro


def get_stick_id():
    """
    Devolve um stick_id persistente:
    - Primeiro tenta ler do ficheiro ~/.stick_id
    - Se não existir, cria usando o serial da Raspberry Pi
    - Depois guarda e usa sempre
    """
    # 1. Se já existir, devolver
    if os.path.exists(STICK_ID_FILE):
        try:
            with open(STICK_ID_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass  # se ficheiro estiver corrompido → recriar

    # 2. Obter serial real
    serial = get_rpi_serial()
    if serial is None:
        # fallback para caso raro
        serial = "0000000000000000"

    # 3. Criar ID numérico a partir do serial
    stick_id = generate_numeric_id(serial)

    # 4. Guardar para uso futuro
    try:
        with open(STICK_ID_FILE, "w") as f:
            f.write(str(stick_id))
    except:
        pass  # caso não consiga escrever, continuar

    return stick_id
