from __future__ import annotations
import json

def resume_crawl_v3(checkpoint: dict):
    payload = (checkpoint or {}).get('checkpoint', '{}')
    try:
        obj = json.loads(payload)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}
