from __future__ import annotations
import re

def extract_api_contracts(text: str):
    src = text or ''
    endpoints = sorted(set(re.findall(r'`(GET|POST|PUT|DELETE|PATCH)\s+([^`]+)`', src)))
    graphql = bool('type Query' in src or 'schema {' in src)
    return {"routes": [{"method": m, "path": p} for m, p in endpoints], "graphql": graphql}
