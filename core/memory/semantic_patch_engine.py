from __future__ import annotations

from typing import Any
from typing import Dict


def build_semantic_patch(
    old: Dict[str, Any],
    new: Dict[str, Any],
) -> Dict[str, Any]:

    added = {}

    removed = {}

    for key in new:

        if key not in old:

            added[key] = new[key]

    for key in old:

        if key not in new:

            removed[key] = old[key]

    return {
        "added": added,
        "removed": removed,
    }
