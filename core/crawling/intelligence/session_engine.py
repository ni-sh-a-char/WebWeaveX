from __future__ import annotations
import json
from core.utils.deterministic_serializer import dumps_deterministic

def checkpoint_session(state: dict):
    return {"checkpoint": dumps_deterministic(state or {})}

def resume_session(checkpoint: dict):
    raw=(checkpoint or {}).get('checkpoint','{}')
    try:
        obj=json.loads(raw)
        return obj if isinstance(obj,dict) else {}
    except Exception:
        return {}
