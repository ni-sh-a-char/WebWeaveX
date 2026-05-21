from __future__ import annotations
import re
def discover_apis(text:str):
    return sorted(set(re.findall(r"/(?:api|v\d+)/[A-Za-z0-9_/-]*", text or "")))
