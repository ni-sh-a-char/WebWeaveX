from __future__ import annotations
import re

def extract_tables(text: str):
    rows=re.findall(r"^\|.*\|$", text or '', flags=re.MULTILINE)
    return {"tables": sorted(set(rows))}
