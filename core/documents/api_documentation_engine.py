from __future__ import annotations
import re

def extract_api_contract_docs(text: str):
    src = text or ""
    routes = sorted(set(re.findall(r"`(GET|POST|PUT|DELETE|PATCH)\s+([^`]+)`", src)))
    return {"routes": [{"method": m, "path": p} for m, p in routes]}
