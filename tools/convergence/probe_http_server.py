"""Minimal HTTP probe server for tests."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '<html><head><title>WebWeaveX Probe</title></head>'
        html += '<body><h1 id="main">Probe Fixture</h1>'
        html += '<p class="headline">Test headline</p>'
        html += '<a href="/alpha">Alpha</a>'
        html += '<a href="/beta">Beta</a>'
        html += '</body></html>'
        self.wfile.write(html.encode('utf-8'))
    def log_message(self, format, *args):
        pass

server = HTTPServer(('127.0.0.1', 8787), Handler)
print('Probe server running on http://127.0.0.1:8787')
sys.stdout.flush()
server.serve_forever()
