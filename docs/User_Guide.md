# AI Against Litter – User Guide

## 1. Clone the Repository

Open a terminal on your Raspberry Pi and clone the repository:

```bash
git clone https://github.com/YourUsername/litter-project.git LitterProject
cd LitterProject
```

Replace `YourUsername` with your GitHub username if needed.

---

## 2. Set Up the Python Virtual Environment

Create a Python virtual environment (`venv_tflite`) and activate it:

```bash
python3 -m venv venv_tflite
source venv_tflite/bin/activate
```

Your prompt should now start with `(venv_tflite)` indicating the environment is active.

---

## 3. Install Dependencies

Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` file, create one with the following packages:

```
tflite-runtime
numpy==1.25.2
opencv-python-headless
pillow
gpiozero
requests
fastapi
python-dotenv
psycopg2-binary
```

> **Note:** The project has been tested on Python 3.11.

---

## 4. Configure the Environment Variables


Create a `.env` file in the project root folder. This file stores sensitive information like the database connection string components (you have to extract them manually by loking at the conection string). Example:


```
DB_HOST=               
DB_NAME=                                                           
DB_USER=                                                          
DB_PASSWORD=                                                       
DB_SSLMODE=                                                                              
```


- **Neon DB**: This project uses Neon DB for storing detection records.
- Place the components of the connection string inside the `.env` file.
- Do **not** commit your `.env` to GitHub.


The code will automatically read the `.env` file using `python-dotenv`.


---

## 5. Create the Automatic Run Script

Create a file called `run_litter.sh` in the home directory for easy execution:

```bash
nano ~/run_litter.sh
```

Paste the following:

```bash
#!/bin/bash
# Activate the Python virtual environment
cd ~/LitterProject
source venv_tflite/bin/activate

# Run the main program
python main.py
```

Make it executable:

```bash
chmod +x ~/run_litter.sh
```

Now you can run the project with:

```bash
~/run_litter.sh
```

---

## 6. Run the Project

Once the environment is active (or using the script):

```bash
source venv_tflite/bin/activate
python main.py
```

When the button is pressed, the system will:

* Capture an image from the camera (fallback to rpicam-still if Picamera2 is unavailable)
* Apply background blurring to emphasize the detected object
* Analyze the material using the TensorFlow Lite model
* Save the processed image locally
* Log the detection as a JSON file
* Send the detection to the database (if configured)

```
Detected Material: Plastic
Saved JSON: /path/to/json_file.json
Image File: /path/to/image.jpg
Saved to DB with ID: 42
URL: http://example.com/view/42
```

---

7. Image Processing (Background Blur)

To improve classification accuracy and visualization, the system applies **background blurring**:

* The main object remains sharp
* The surrounding background is blurred
* The blurred image is the one saved and displayed
* The original image is not used after processing
This helps reduce visual noise and makes detections clearer for both users and reviewers.

---

8. Local Web Interface

A lightweight local web server is started automatically.

**Accessing the interface**

From another device on the same network, open:
```
http://<raspberry-pi-ip>:8000  (the ip can be, by default, "raspberrypi")
```
**Behavior**
* Displays all images captured during the current session
* Images are shown in chronological order
* The page does not auto-refresh
* Refresh manually (F5) to see new images
* No continuous background requests are made

---

9. Database Integration

If database credentials are provided in the ```.env``` file:

* Each detection is sent to the database
* Stored data includes:
    * Material type
    * Timestamp
    * Image URL
    * GPS location
    * Device ID
If the database is unreachable, the system continues operating locally without interruption.

---

## 10. Notes for the Raspberry Pi

* Ensure the Pi’s camera is enabled in `raspi-config`.
* The GPIO buzzer is connected to **GPIO17 (BOARD pin 11)** on a perfboard with a 2x20 connector.
* If running headless (without a monitor), you can still SSH into the Pi and run the script.

---

## 11. References

* Model source: [WasteNet Garbage Classifier](https://github.com/KrisnaSantosa15/wastenet-garbage-classifier/tree/main)
* TensorFlow Lite: [https://www.tensorflow.org/lite](https://www.tensorflow.org/lite)
* GPIOZero documentation: [https://gpiozero.readthedocs.io](https://gpiozero.readthedocs.io)
