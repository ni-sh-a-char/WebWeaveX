from __future__ import annotations

from typing import Any, Dict, List


def check_graph_invariants(graph: Dict[str, Any]) -> Dict[str, Any]:
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    node_ids = {n.get("id") for n in nodes if isinstance(n, dict) and n.get("id")}
    violations: List[Dict[str, str]] = []
    for e in edges:
        if not isinstance(e, dict):
            continue
        if "type" in e:
            violations.append({"rule": "no_edge_type", "edge": str(e.get("from"))})
        if e.get("from") not in node_ids or e.get("to") not in node_ids:
            if node_ids:
                violations.append({"rule": "dangling_edge", "from": str(e.get("from")), "to": str(e.get("to"))})
    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "deterministic_inputs": [f"violations={len(violations)}"],
    }
