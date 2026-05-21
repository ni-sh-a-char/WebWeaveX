from __future__ import annotations
import re

def parse_protobuf(text: str):
    src = text or ''
    messages = sorted(set(re.findall(r'\bmessage\s+([A-Za-z_][A-Za-z0-9_]*)\b', src)))
    services = sorted(set(re.findall(r'\bservice\s+([A-Za-z_][A-Za-z0-9_]*)\b', src)))
    return {"messages": messages, "services": services}
