from __future__ import annotations

from typing import Any, Dict, List


def build_adaptive_runtime_graph(
    adaptation: Dict[str, Any],
) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    fallback = adaptation.get("fallback", {}).get("chain", [])

    for step in fallback:
        node_id = f"fallback_{step.get('step', 0)}"
        nodes.append({
            "id": node_id,
            "type": "fallback",
            "strategy": step.get("strategy"),
        })

        step_index = int(step.get("step", 0))
        if step_index > 0:
            edges.append({
                "from": f"fallback_{step_index - 1}",
                "to": node_id,
                "relation": "fallback_next",
            })

    return {
        "ir": "adaptive_runtime_graph",
        "nodes": nodes,
        "edges": edges,
        "bounded": True,
    }
