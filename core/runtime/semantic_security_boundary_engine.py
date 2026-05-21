from __future__ import annotations

from typing import Any, Dict


def validate_semantic_boundary(
    payload: Dict[str, Any],
) -> Dict[str, Any]:

    blocked = any(
        key.lower().startswith("__")
        for key in payload.keys()
    )

    return {
        "accepted": not blocked,
        "blocked": blocked,
    }
