from __future__ import annotations
import json

def parse_openapi(text: str):
    src = text or ''
    try:
        obj = json.loads(src)
    except Exception:
        obj = {}
    paths = sorted((obj.get('paths') or {}).keys()) if isinstance(obj, dict) else []
    return {"paths": paths, "version": str((obj.get('openapi') if isinstance(obj, dict) else '') or '')}
