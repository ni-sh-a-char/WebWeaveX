from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

MAX_GRAPH_NODES = 5000
MAX_GRAPH_EDGES = 20000


def build_semantic_graph(parsed: Dict[str, Any]) -> Dict[str, Any]:
    symbols = parsed.get("symbols", {}) or {}
    imports = parsed.get("imports", {}) or {}
    calls = parsed.get("calls", {}) or {}
    source_id = str(parsed.get("source_id") or parsed.get("language") or "module")

    node_ids: Set[str] = {source_id}
    for key in ("classes", "functions", "interfaces", "symbols"):
        for name in symbols.get(key, []) or []:
            node_ids.add(str(name))
    for edge in imports.get("edges", []) or []:
        if isinstance(edge, dict):
            node_ids.add(str(edge.get("to", "")))

    edge_meta: Dict[Tuple[str, str], str] = {}
    for edge in imports.get("edges", []) or []:
        if isinstance(edge, dict) and edge.get("from") and edge.get("to"):
            key = (str(edge["from"]), str(edge["to"]))
            edge_meta[key] = "observed"
    for edge in calls.get("calls", []) or []:
        if isinstance(edge, dict) and edge.get("from") and edge.get("to"):
            f, t = str(edge["from"]), str(edge["to"])
            node_ids.add(f)
            node_ids.add(t)
            key = (f, t)
            edge_meta[key] = edge_meta.get(key, "inferred") if key in edge_meta else "observed"

    nodes = [
        {"id": nid, "kind": "symbol", "metadata": {}}
        for nid in sorted(n for n in node_ids if n)[:MAX_GRAPH_NODES]
    ]
    allowed = {n["id"] for n in nodes}
    edge_list = [
        {
            "from": f,
            "to": t,
            "metadata": {"edge_basis": edge_meta.get((f, t), "observed"), "evidence": ["parser:graph"]},
        }
        for f, t in sorted(edge_meta.keys())
        if f in allowed and t in allowed
    ][:MAX_GRAPH_EDGES]

    return {"nodes": nodes, "edges": edge_list, "max_edges": MAX_GRAPH_EDGES}
