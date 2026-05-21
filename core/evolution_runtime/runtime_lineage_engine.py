from __future__ import annotations

from typing import Any, Dict, List


def build_runtime_lineage(
    evolution_id: str,
    mutations: List[Dict[str, Any]],
    parent_id: str = "",
) -> List[Dict[str, Any]]:
    lineage: List[Dict[str, Any]] = []

    if parent_id:
        lineage.append({
            "id": parent_id,
            "relation": "parent",
        })

    lineage.append({
        "id": evolution_id,
        "relation": "current",
    })

    for mutation in mutations[:1000]:
        lineage.append({
            "id": f"{mutation.get('kind', '')}:{mutation.get('target', '')}",
            "relation": "mutation",
            "ancestor": evolution_id,
        })

    return sorted(lineage, key=lambda item: str(item.get("id", "")))
