# send_to_server.py
import requests
import os

API_URL = os.getenv("SERVER_API_URL")  # define no .env, ex: https://example.com/api/upload
API_KEY = os.getenv("SERVER_API_KEY")  # opcional, se precisa de autenticação

def send_to_server(json_path, image_path):
    if API_URL is None:
        print("SERVER_API_URL not defined in .env")
        return False

    if not os.path.exists(json_path) or not os.path.exists(image_path):
        print("Files do not exist, cannot send.")
        return False

    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    with open(image_path, "rb") as f_img, open(json_path, "r") as f_json:
        files = {
            "image": ("image.jpg", f_img, "image/jpeg"),
            "metadata": ("metadata.json", f_json, "application/json")
        }
        try:
            response = requests.post(API_URL, headers=headers, files=files, timeout=10)
            response.raise_for_status()
            print("Upload successful:", response.status_code)
            return True
        except requests.exceptions.RequestException as e:
            print("Error uploading:", e)
            return False
