from __future__ import annotations
import re

def parse_graphql(text: str):
    src = text or ''
    types = sorted(set(re.findall(r'\btype\s+([A-Za-z_][A-Za-z0-9_]*)\b', src)))
    queries = sorted(set(re.findall(r'\bquery\s+([A-Za-z_][A-Za-z0-9_]*)\b', src)))
    return {"types": types, "queries": queries}
