from __future__ import annotations

from typing import Any, Dict


def diff_evolution_runtime(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    prev_id = str(previous.get("evolution_id", ""))
    curr_id = str(current.get("evolution_id", ""))

    return {
        "evolution_changed": prev_id != curr_id,
        "previous_id": prev_id,
        "current_id": curr_id,
        "mutation_delta": len(current.get("mutations", [])) - len(previous.get("mutations", [])),
        "revertible": True,
        "bounded": True,
    }
