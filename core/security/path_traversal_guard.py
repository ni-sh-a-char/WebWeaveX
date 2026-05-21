from __future__ import annotations
def safe_path(path:str):
    p=(path or "").replace("\\","/")
    return "../" not in p and not p.startswith("/")
