# AI Against Litter

## Project Overview
AI Against Litter is an embedded AI system designed to assist in litter collection by automatically identifying waste materials using computer vision and a TensorFlow Lite model.  
The system is designed to be integrated into a litter picker tool and runs on a Raspberry Pi 5.

This project was developed as part of an academic assignment at **Avans University of Applied Sciences – ETP**.

---

## Features
- Image capture using Raspberry Pi Camera
- Waste material classification using TensorFlow Lite
- Background blurring to emphasize the detected object
- Audible feedback via buzzer
- Local JSON logging
- Local web interface to view captured images
- Optional database integration
- Designed for offline operation

---

## Hardware Used
- Raspberry Pi 5
- Raspberry Pi Camera Module 3, Wide
- Buzzer (GPIO)
- Push button (GPIO)
- Perfboard connected to Raspberry Pi 40-pin header
- Litter picker mechanical structure

---

## Software Stack
- Python 3.11
- TensorFlow Lite Runtime
- OpenCV (headless)
- NumPy (< 2.0)
- GPIO Zero
- FastAPI (local web server)
- PostgreSQL (Neon DB)

---

## AI Model
The waste classification model is based on **WasteNet** and converted to TensorFlow Lite.

Original repository:
https://github.com/KrisnaSantosa15/wastenet-garbage-classifier

All credit for the original model architecture and dataset goes to the original author.

---

## Local Web Interface
The system starts a lightweight local web server that allows viewing **all images captured during the current session**.

- Images are updated **only when a new detection occurs**
- The page does **not auto-refresh**
- Manual refresh (`F5`) shows the latest images
- Each image shown corresponds to a processed (blurred-background) result

---

## Documentation
Documentation is available in the `docs/` folder
For detailed instructions on setup and execution, please refer to:

📄 `docs/User_Guide.md`
📄 `docs/Hardware_Setup.md`

---

## Academic Context
- Project Name: **AI Against Litter**
- Institution: **Avans University of Applied Sciences**
- Program: **ETP**
