from __future__ import annotations

from typing import Any, Dict, List


MAX_EDGES = 500


def map_distributed_dependencies(
    services: List[Dict[str, Any]],
) -> Dict[str, Any]:
    edges = []
    names = sorted({str(s.get("name", "")) for s in services})
    for idx in range(1, len(names)):
        edges.append(
            {
                "from": names[idx - 1],
                "to": names[idx],
                "metadata": {"kind": "service_order", "basis": "lexicographic"},
            }
        )
    return {"edges": edges[:MAX_EDGES], "count": min(len(edges), MAX_EDGES), "deterministic": True}
