from __future__ import annotations

from typing import Any, Dict, List


MAX_DEPS = 500


def resolve_runtime_dependencies(
    nodes: List[str],
    edges: List[Dict[str, Any]],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    adj: Dict[str, List[str]] = {}
    for e in edges[:MAX_DEPS]:
        if not isinstance(e, dict):
            continue
        src, dst = e.get("from"), e.get("to")
        if src and dst:
            adj.setdefault(str(src), []).append(str(dst))
    for k in adj:
        adj[k] = sorted(set(adj[k]))
    return {
        "adjacency": adj,
        "nodes": sorted(set(nodes))[:MAX_DEPS],
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
