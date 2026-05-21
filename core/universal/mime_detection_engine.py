from __future__ import annotations
def detect_mime(text:str):
    t=(text or "").lstrip()
    if t.startswith("<"): return "text/html"
    if t.startswith("{") or t.startswith("["): return "application/json"
    return "text/plain"
