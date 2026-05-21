from __future__ import annotations

from typing import Any, Dict, List

from core.runtime_graph.runtime_graph_engine import build_runtime_graph

MAX_RUNTIMES = 1000


def federate_extraction_runtimes(
    runtimes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    graphs = []

    for runtime in runtimes[:MAX_RUNTIMES]:
        if runtime.get("nodes") or runtime.get("edges"):
            graphs.append(runtime)

    merged = build_runtime_graph(graphs) if graphs else {
        "ir": "unified_runtime_graph",
        "nodes": [],
        "edges": [],
        "bounded": True,
    }

    return {
        "topology": merged,
        "runtime_count": len(runtimes[:MAX_RUNTIMES]),
        "bounded": True,
    }
