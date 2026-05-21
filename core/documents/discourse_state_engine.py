from __future__ import annotations

from typing import Any, Dict, List


def track_discourse_state(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(sections, key=lambda s: int(s.get("order", 0)))
    current = ordered[-1].get("id") if ordered else None
    return {"current_section": current, "depth": len(ordered), "deterministic": True}
