from __future__ import annotations

from typing import Any, Dict


def detect_recursive_narrative_monopoly(narrative_count: int, depth: int) -> Dict[str, Any]:
    monopoly = narrative_count <= 1 and depth >= 2
    return {"monopoly": monopoly, "suppress": monopoly, "lock_in_blocked": True}
