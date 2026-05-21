from __future__ import annotations

from typing import Any, Dict, List


def track_runtime_mutations(
    changes: List[Dict[str, Any]],
    tick: int = 0,
) -> Dict[str, Any]:
    return {
        "mutations": sorted(changes, key=lambda item: str(item.get("field", ""))),
        "count": len(changes),
        "tick": tick,
        "bounded": True,
    }
