from __future__ import annotations

from typing import Any, Dict


def build_semantic_cognitive_lineage(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:

    lineage = sorted(
        runtime.keys()
    )

    return {
        "lineage": lineage,
        "lineage_depth": len(
            lineage
        ),
    }
