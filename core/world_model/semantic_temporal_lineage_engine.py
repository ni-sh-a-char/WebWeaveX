from __future__ import annotations

from typing import Any, Dict, List


def build_semantic_temporal_lineage(
    snapshots: List[Dict[str, Any]],
) -> Dict[str, Any]:

    ordered = []

    for idx, snapshot in enumerate(
        snapshots
    ):

        ordered.append(
            {
                "timestamp": idx,
                "snapshot": snapshot,
            }
        )

    return {
        "timeline": ordered,
    }
