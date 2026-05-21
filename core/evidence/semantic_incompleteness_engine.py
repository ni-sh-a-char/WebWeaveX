from __future__ import annotations

from typing import Any, Dict, List


def model_incompleteness(
    known: Dict[str, Any],
    unknown: List[str],
    unsupported: List[str],
) -> Dict[str, Any]:
    return {
        "known": known,
        "unknown": sorted(set(unknown or [])),
        "unsupported": sorted(set(unsupported or [])),
        "incomplete": bool(unknown or unsupported),
        "preserved": True,
    }
