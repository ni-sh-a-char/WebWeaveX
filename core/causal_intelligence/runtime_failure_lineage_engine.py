from __future__ import annotations

from typing import Any, Dict, List


MAX_LINEAGE = 1000


def build_runtime_failure_lineage(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    conflicts = runtime_ir.get(
        "runtime_conflicts",
        {},
    )

    conflict_items = list(
        conflicts.get(
            "conflicts",
            [],
        )
        if isinstance(conflicts, dict)
        else []
    )

    lineage: List[Dict[str, Any]] = []

    for idx, conflict in enumerate(
        conflict_items
    ):

        lineage.append(
            {
                "id": f"failure_{idx}",
                "origin": str(conflict),
                "severity": "structural",
            }
        )

    return {
        "failure_lineage": lineage[:MAX_LINEAGE],
        "bounded": True,
    }
