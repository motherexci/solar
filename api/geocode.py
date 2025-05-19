from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from pgeocode import Nominatim

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1) parse the “zip” query parameter
        params = parse_qs(urlparse(self.path).query)
        zip_code = params.get("zip", [None])[0]
        if not zip_code:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'zip' parameter"}).encode())
            return

        # 2) look up latitude & longitude
        nomi = Nominatim("us")
        location = nomi.query_postal_code(zip_code)
        try:
            lat = float(location.latitude)
            lon = float(location.longitude)
        except Exception:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"ZIP '{zip_code}' not found"}).encode())
            return

        # 3) return JSON
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"latitude": lat, "longitude": lon}).encode())
