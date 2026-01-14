import subprocess
import threading

def start_cloudflare_tunnel():
    print("[Cloudflare] Starting tunnel...")
    subprocess.Popen(
        [
            "cloudflared",
            "tunnel",
            "--url",
            "http://localhost:8000"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run_in_thread():
    thread = threading.Thread(target=start_cloudflare_tunnel, daemon=True)
    thread.start()
