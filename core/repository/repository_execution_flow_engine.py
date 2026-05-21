from __future__ import annotations

from typing import Any, Dict, List

MAX_FLOWS = 10000


def reconstruct_execution_flows(
    dependencies: Dict[str, Any],
) -> Dict[str, Any]:
    flows: List[Dict[str, Any]] = []

    for edge in dependencies.get("edges", []):
        flows.append({
            "from": edge.get("from"),
            "to": edge.get("to"),
            "relation": edge.get("relation", "imports"),
        })

    for dep in dependencies.get("imports", []):
        flows.append({
            "from": "module",
            "to": dep,
            "relation": "imports",
        })

        if len(flows) >= MAX_FLOWS:
            break

    return {
        "flows": sorted(
            flows,
            key=lambda x: (
                str(x.get("from")),
                str(x.get("to")),
            ),
        )[:MAX_FLOWS],
        "bounded": True,
    }
