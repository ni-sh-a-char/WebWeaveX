from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_KEYS = ("goal",)


def validate_semanticity(
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    missing = [
        key
        for key in REQUIRED_KEYS
        if not payload.get(key)
    ]
    return {
        "semantic": not missing,
        "missing_keys": missing,
    }
