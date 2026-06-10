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


def canonicalize_number(value: Any) -> Any:
    """Cross-language numeric canonicalization.

    JavaScript has a single number type, so 2.0 cannot serialize differently
    from 2. Contract: integral floats serialize as integers, non-finite floats
    as null — identically in Python, JavaScript, and Dart. 2**63 bounds the
    range where the conversion is exact in every runtime.
    """
    if isinstance(value, float) and not isinstance(value, bool):
        if value != value or value in (float("inf"), float("-inf")):
            return None
        if value.is_integer() and abs(value) < 9223372036854775808.0:
            return int(value)
    return value


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
                stable_sort_keys(item) if isinstance(item, dict) else canonicalize_number(item)
                for item in val
            ]
        else:
            sorted_obj[key] = canonicalize_number(val)
    return sorted_obj


def _canonicalize_numbers_deep(value: Any) -> Any:
    """Apply canonicalize_number at every depth (lists nested in lists included),
    matching the JavaScript and Dart canonical encoders which canonicalize at
    serialization time."""
    if isinstance(value, dict):
        return {k: _canonicalize_numbers_deep(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_canonicalize_numbers_deep(v) for v in value]
    return canonicalize_number(value)


def stable_serialize(value: Any) -> str:
    if isinstance(value, str):
        return normalize_runtime_value(value)
    if isinstance(value, dict):
        return json.dumps(
            _canonicalize_numbers_deep(stable_sort_keys(value)),
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
        return json.dumps(
            _canonicalize_numbers_deep(keyed),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return json.dumps(canonicalize_number(value), ensure_ascii=False, separators=(",", ":"))
