from __future__ import annotations

from typing import Any, Dict


def diff_semantic_repository(
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Any]:

    left_keys = set(left.keys())
    right_keys = set(right.keys())

    return {
        "added": sorted(
            right_keys - left_keys
        ),
        "removed": sorted(
            left_keys - right_keys
        ),
    }
