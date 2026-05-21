from __future__ import annotations

import json
from typing import Any, Dict

from core.schemas.normalized_schema import empty_normalized


def _sort_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _sort_value(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        normalized = [_sort_value(v) for v in value]
        return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=True))
    return value


def normalize_output(parts: Dict[str, Any], source_url: str = "") -> Dict[str, Any]:
    out = empty_normalized(source_url=source_url)
    for key in ("content", "code", "dependencies", "metadata", "relationships"):
        if key in parts and isinstance(parts[key], dict):
            out[key] = _sort_value(parts[key])
    out["raw_text"] = str(parts.get("raw_text", "") or "")
    out["source_url"] = source_url or str(parts.get("source_url", "") or "")
    out["fingerprint"] = str(parts.get("fingerprint", "") or "")
    return out

