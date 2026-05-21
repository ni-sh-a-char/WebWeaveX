from __future__ import annotations
import json
def parse_structured(text:str):
    try: return json.loads(text or "{}")
    except Exception: return {}
