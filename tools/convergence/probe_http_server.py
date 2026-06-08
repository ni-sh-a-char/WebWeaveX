#!/usr/bin/env python3
"""Deterministic local HTTP server for certification probes.

Serves fixed content so Python and JavaScript fetchers can be compared on
their success paths without external network variance.
"""
from __future__ import annotations

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8787

BODY_HTML = (
    "<html><head><title>WebWeaveX Probe</title></head>"
    '<body><h1 id="main" class="headline">Probe Fixture</h1>'
    '<p>Deterministic content for parity certification.</p>'
    '<a href="/alpha">alpha</a> <a href="/beta">beta</a>'
    "<pre>code block</pre>"
    "</body></html>"
)

BODY_404 = "<html><body>not found</body></html>"


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):  # noqa: N802
        if self.path == "/probe" or self.path == "/":
            body = BODY_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            body = BODY_404.encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # noqa: D102
        pass


def main() -> int:
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"probe server on {PORT}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
