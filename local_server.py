import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(BASE_DIR, "output", "frames")
WEB_DIR = os.path.join(BASE_DIR, "web")


def latest_session():
    sessions = [d for d in os.listdir(FRAMES_DIR) if d.startswith("session_")]
    return max(sessions) if sessions else None


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/images.json":
            session = latest_session()
            images = []

            if session:
                p = os.path.join(FRAMES_DIR, session)
                images = sorted(
                    f"/output/frames/{session}/{f}"
                    for f in os.listdir(p) if f.endswith(".jpg")
                )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(images).encode())
            return

        if self.path == "/" or self.path == "/index.html":
            self.path = "/web/index.html"

        return super().do_GET()


def run_in_thread(port=8000):
    os.chdir(BASE_DIR)
    server = HTTPServer(("0.0.0.0", port), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    print(f"🌐 Web server running on port {port}")
