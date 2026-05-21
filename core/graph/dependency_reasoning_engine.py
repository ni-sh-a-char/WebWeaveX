from __future__ import annotations

from typing import Dict, List, Set


def reason_dependencies(graph: Dict[str, object]) -> Dict[str, object]:
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    deps: Dict[str, Set[str]] = {}
    for e in edges:
        if not isinstance(e, dict):
            continue
        f, t = str(e.get("from", "")), str(e.get("to", ""))
        if not f or not t:
            continue
        deps.setdefault(f, set()).add(t)
    chains = sorted(
        [{"from": f, "to": sorted(ts)} for f, ts in deps.items()],
        key=lambda x: x["from"],
    )[:500]
    return {"dependency_chains": chains, "root_count": len(deps)}
