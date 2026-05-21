from __future__ import annotations
import json

def parse_adaptive(text: str, fmt: str):
    src = text or ""
    if fmt == 'json':
        try:
            obj = json.loads(src)
            if isinstance(obj, dict): return {"kind": "json-object", "keys": sorted(obj.keys())}
            if isinstance(obj, list): return {"kind": "json-array", "length": len(obj)}
        except Exception:
            return {"kind": "json-invalid"}
    return {"kind": f"{fmt}-text", "length": len(src)}
