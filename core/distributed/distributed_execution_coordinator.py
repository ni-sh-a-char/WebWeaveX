from __future__ import annotations

from typing import Any, Dict, List


def coordinate_distributed_execution(
    schedules: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = sorted(
        schedules,
        key=lambda x: str(x),
    )

    return {
        "coordinated": ordered,
        "count": len(ordered),
    }
