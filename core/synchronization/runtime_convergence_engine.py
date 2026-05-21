from __future__ import annotations

from typing import Any, Dict, List


def converge_runtime_state(
    realities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    histories: List[str] = []

    for index, reality in enumerate(sorted(realities, key=lambda item: str(item.get("reality_id", "")))):
        reality_id = str(reality.get("reality_id", f"reality:{index}"))
        histories.append(reality_id)
        for key, value in reality.items():
            if key == "reality_id":
                continue
            if key not in merged:
                merged[key] = value
            elif merged[key] != value:
                merged[key] = value

    return {
        "converged_state": merged,
        "reality_count": len(realities),
        "histories": histories,
        "converged": True,
        "bounded": True,
    }
