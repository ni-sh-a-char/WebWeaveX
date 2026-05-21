from __future__ import annotations
def detect_protocol(url:str):
    u=(url or "").lower()
    return "https" if u.startswith("https://") else ("http" if u.startswith("http://") else "unknown")
