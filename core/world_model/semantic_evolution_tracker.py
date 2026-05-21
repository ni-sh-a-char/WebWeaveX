from __future__ import annotations

from typing import Any, Dict, List


def track_semantic_evolution(
    versions: List[Dict[str, Any]],
) -> Dict[str, Any]:

    lineage = []

    for idx, version in enumerate(
        versions
    ):

        lineage.append(
            {
                "version": idx,
                "state": version,
            }
        )

    return {
        "lineage": lineage,
        "depth": len(lineage),
    }
