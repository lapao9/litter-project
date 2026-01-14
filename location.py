import urllib.request
import json

def get_location():
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=3) as r:
            data = json.load(r)
            loc = data.get("loc")
            if not loc:
                return None, None
            lat, lon = loc.split(",")
            return float(lat), float(lon)
    except Exception as e:
        print("Location error:", e)
        return None, None
