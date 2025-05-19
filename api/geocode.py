from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1) parse the “zip” query parameter
        params = parse_qs(urlparse(self.path).query)
        zip_code = params.get("zip", [None])[0]
        if not zip_code:
            return self._send_json(400, {"error": "Missing 'zip' parameter"})

        # 2) call external geocoding API
        resp = requests.get(f"https://api.zippopotam.us/us/{zip_code}")
        if resp.status_code != 200:
            return self._send_json(404, {"error": f\"ZIP '{zip_code}' not found\"})

        data = resp.json()
        place = data["places"][0]
        lat = float(place["latitude"])
        lon = float(place["longitude"])

        # 3) return JSON
        return self._send_json(200, {"latitude": lat, "longitude": lon})

    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
