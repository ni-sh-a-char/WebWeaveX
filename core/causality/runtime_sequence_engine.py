from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_sequence(
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ordered = sorted(events, key=lambda item: int(item.get("step", 0)))

    return {
        "sequence": [
            {
                "id": str(event.get("id", "")),
                "runtime": str(event.get("runtime", "")),
                "type": str(event.get("type", "")),
                "step": int(event.get("step", index)),
            }
            for index, event in enumerate(ordered[:10000])
        ],
        "length": len(ordered),
        "bounded": True,
    }
