from __future__ import annotations

from typing import Any, Dict, List


def schedule_kernel_phases(
    phases: List[str],
    tick: int = 0,
) -> Dict[str, Any]:
    scheduled = [
        {"phase": phase, "tick": tick + index, "priority": index}
        for index, phase in enumerate(phases)
    ]
    return {
        "scheduled": sorted(scheduled, key=lambda item: item["priority"]),
        "deterministic": True,
        "bounded": True,
    }
