from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import sys

# Import the recognize_batch function from xViewer
from xLogic_web_viewer import recognize_batch

# Import the get_all_properties function from xViewer
from xLogic_web_viewer import get_all_properties

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/recognize_batch':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Call the recognize_batch function here
            results = recognize_batch()
            self.wfile.write(json.dumps(results).encode())
        elif self.path == '/get_properties':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Call the get_all_properties function here
            properties = get_all_properties()
            self.wfile.write(json.dumps(properties).encode())
        else:
            super().do_GET()

def start_recognize_server(addr="localhost", port=8081):
    httpd = HTTPServer((addr, port), CustomHandler)
    print(f"Serving HTTP on {addr} port {port} (http://{addr}:{port}/) ...")
    httpd.serve_forever()

if __name__ == "__main__":
    start_recognize_server()