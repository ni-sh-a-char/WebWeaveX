"""Cross-language normalization — must match javascript/src/determinism/normalization.ts."""
from __future__ import annotations

import json
import re
import unicodedata
from typing import Any

VOLATILE_RUNTIME_KEYS = frozenset(
    {
        "timestamp",
        "created_at",
        "updated_at",
        "nonce",
        "request_id",
        "csrf",
        "generated_at",
        "runtime_id",
        "random",
        "uuid",
    }
)


def normalize_runtime_value(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\s+$", "", normalized)


def stable_sort_keys(obj: dict[str, Any]) -> dict[str, Any]:
    sorted_obj: dict[str, Any] = {}
    for key in sorted(obj.keys()):
        if key in VOLATILE_RUNTIME_KEYS:
            continue
        val = obj[key]
        if isinstance(val, dict):
            sorted_obj[key] = stable_sort_keys(val)
        elif isinstance(val, list):
            sorted_obj[key] = [
                stable_sort_keys(item) if isinstance(item, dict) else item for item in val
            ]
        else:
            sorted_obj[key] = val
    return sorted_obj


def stable_serialize(value: Any) -> str:
    if isinstance(value, str):
        return normalize_runtime_value(value)
    if isinstance(value, dict):
        return json.dumps(
            stable_sort_keys(value),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    if isinstance(value, list):
        # JavaScript stableSerialize treats arrays as keyed objects (fast-json-stable-stringify).
        keyed = {
            str(i): stable_sort_keys(item) if isinstance(item, dict) else item
            for i, item in enumerate(value)
        }
        return json.dumps(keyed, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
