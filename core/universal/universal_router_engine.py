from __future__ import annotations
def route_input(source:str):
    s=(source or "").lower();
    if s.startswith("http"): return "web"
    if s.endswith(".pdf"): return "pdf"
    if s.endswith(".json"): return "json"
    return "text"
