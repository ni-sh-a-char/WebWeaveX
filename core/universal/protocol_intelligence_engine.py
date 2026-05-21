from __future__ import annotations

from urllib.parse import urlparse


def detect_protocol_intelligence(source: str):
    p = urlparse(source or "")
    scheme = (p.scheme or "unknown").lower()
    host = (p.netloc or "").lower()
    return {"scheme": scheme, "host": host}
