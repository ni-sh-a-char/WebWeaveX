from __future__ import annotations

from typing import Any, Dict, List


def model_capture_resistance(suppressed: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "resistant": True,
        "capture_events_suppressed": len(suppressed),
        "domination_blocked": bool(suppressed),
    }
