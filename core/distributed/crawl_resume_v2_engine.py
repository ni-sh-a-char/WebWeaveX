from __future__ import annotations

import json


def resume_crawl_v2(checkpoint: dict):
    payload = (checkpoint or {}).get("checkpoint", "{}")
    try:
        data = json.loads(payload)
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data
