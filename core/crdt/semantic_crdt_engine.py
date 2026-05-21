from __future__ import annotations

from typing import Any
from typing import Dict


def merge_semantic_states(
    left: Dict[str, Any],
    right: Dict[str, Any],
) -> Dict[str, Any]:

    merged = dict(left)

    for key, value in right.items():

        if key not in merged:
            merged[key] = value
            continue

        if merged[key] != value:

            merged[key] = sorted([
                merged[key],
                value,
            ])

    return {
        "state": merged,
        "merged": True,
    }
