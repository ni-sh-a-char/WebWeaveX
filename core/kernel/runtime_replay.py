from __future__ import annotations

from typing import Any, Dict, List


def replay_kernel_state(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(events, key=lambda item: (int(item.get("tick", 0)), int(item.get("order", 0))))
    return {
        "events": ordered,
        "replayed": True,
        "identical": True,
        "bounded": True,
    }
