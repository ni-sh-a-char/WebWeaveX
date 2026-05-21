from __future__ import annotations

from typing import Any, Dict, List


def coordinate_kernel_phases(
    phase_results: List[Dict[str, Any]],
    tick: int = 0,
) -> Dict[str, Any]:
    ordered = sorted(phase_results, key=lambda item: str(item.get("phase", "")))
    return {
        "phases": ordered,
        "tick": tick,
        "coordinated": True,
        "bounded": True,
    }
