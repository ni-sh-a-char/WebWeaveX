from __future__ import annotations
import re

def extract_dependency_references(text: str):
    src = text or ''
    refs = sorted(set(re.findall(r'(?:pip install|npm install|cargo add|pub add)\s+([A-Za-z0-9_.@/-]+)', src)))
    return {"dependencies": refs}
