from __future__ import annotations

import json


def extract_structured_payload(text: str):
    raw = text or ""
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {"kind": "json", "keys": sorted(parsed.keys())}
        if isinstance(parsed, list):
            return {"kind": "json", "length": len(parsed)}
    except Exception:
        pass

    if "<" in raw and ">" in raw:
        return {"kind": "markup", "length": len(raw)}
    if ":" in raw and "\n" in raw:
        return {"kind": "key_value_text", "length": len(raw)}
    return {"kind": "text", "length": len(raw)}
