import http.server
import socketserver
import threading
import os

PORT = 8000
BASE_DIR = os.path.abspath(".")

def start_http_server():
    os.chdir(BASE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[HTTP] Serving {BASE_DIR} at port {PORT}")
        httpd.serve_forever()

def run_in_thread():
    thread = threading.Thread(target=start_http_server, daemon=True)
    thread.start()
