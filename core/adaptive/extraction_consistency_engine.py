from __future__ import annotations

from typing import Any, Dict, List


def verify_extraction_consistency(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    previous_fields = set(previous.get("fields", []))
    current_fields = set(current.get("fields", []))

    return {
        "stable": previous_fields == current_fields,
        "added": sorted(current_fields - previous_fields),
        "removed": sorted(previous_fields - current_fields),
        "bounded": True,
    }
