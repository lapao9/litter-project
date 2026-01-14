# User Guide  
## AI Against Litter

---

## 1. Accessing the Raspberry Pi

### 1.1 Power On
Connect power to the Raspberry Pi.  
The system is configured to start automatically on boot.

### 1.2 SSH Access
If a network is available:
```bash
ssh pi@raspberrypi
password = 1234
```

## 2. Running the Application Manually
```bash
cd ~/litter-project
source venv_tflite/bin/activate
python main.py
```

Or using the helper script:

```bash
~/run_litter.sh
```
