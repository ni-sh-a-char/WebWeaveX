from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

MAX_NODES = 5000
MAX_EDGES = 20000


def _node_id(value: Any) -> str:
    return str(value or "").strip()


def normalize_graph_nodes(graph: Dict[str, Any]) -> Dict[str, Any]:
    nodes = []
    for raw in graph.get("nodes", []) or []:
        if isinstance(raw, str):
            nodes.append({"id": _node_id(raw), "kind": "structural", "metadata": {}})
            continue
        if not isinstance(raw, dict):
            continue
        nid = _node_id(raw.get("id"))
        if not nid:
            continue
        kind = raw.get("kind") or "structural"
        metadata = raw.get("metadata") if isinstance(raw.get("metadata"), dict) else {}
        nodes.append({"id": nid, "kind": str(kind), "metadata": metadata})
    return {**graph, "nodes": nodes}


def reconstruct_graph(
    system_graph: Dict[str, Any],
    max_edges: int = MAX_EDGES,
    max_nodes: int = MAX_NODES,
) -> Dict[str, Any]:
    if not isinstance(system_graph, dict):
        return {"nodes": [], "edges": [], "max_edges": max_edges}

    raw_nodes = system_graph.get("nodes", []) or []
    raw_edges = system_graph.get("edges", []) or []
    components = system_graph.get("components", []) or []
    relationships = system_graph.get("relationships", []) or []

    node_set: Set[str] = set()
    for n in raw_nodes:
        if isinstance(n, dict):
            node_set.add(_node_id(n.get("id")))
        else:
            node_set.add(_node_id(n))
    for c in components:
        if isinstance(c, dict):
            node_set.add(_node_id(c.get("name")))

    edge_set: Set[Tuple[str, str]] = set()
    merged_edges: List[dict] = []
    merged_edges.extend(raw_edges if isinstance(raw_edges, list) else [])
    merged_edges.extend(relationships if isinstance(relationships, list) else [])
    for e in merged_edges:
        if not isinstance(e, dict):
            continue
        if "type" in e:
            continue
        f = _node_id(e.get("from"))
        t = _node_id(e.get("to"))
        if not f or not t:
            continue
        node_set.add(f)
        node_set.add(t)
        edge_set.add((f, t))

    nodes = [
        {"id": nid, "kind": "structural", "metadata": {}}
        for nid in sorted(n for n in node_set if n)[:max_nodes]
    ]
    allowed = {n["id"] for n in nodes}
    edges = [
        {"from": f, "to": t}
        for f, t in sorted(edge_set)
        if f in allowed and t in allowed
    ][:max_edges]
    return {"nodes": nodes, "edges": edges, "max_edges": max_edges}


def build_semantic_graph_from_ids(
    node_ids: List[str],
    edges: List[dict],
    max_nodes: int = MAX_NODES,
    max_edges: int = MAX_EDGES,
) -> Dict[str, Any]:
    raw_nodes = [{"id": str(n), "kind": "structural", "metadata": {}} for n in node_ids if n]
    return reconstruct_graph(
        {"nodes": raw_nodes, "edges": edges},
        max_edges=max_edges,
        max_nodes=max_nodes,
    )


def bound_graph_memory(
    graph: Dict[str, Any],
    max_nodes: int = MAX_NODES,
    max_edges: int = MAX_EDGES,
) -> Dict[str, Any]:
    return reconstruct_graph(graph, max_edges=max_edges, max_nodes=max_nodes)


def score_graph(graph: Dict[str, Any]) -> Dict[str, object]:
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "density": round(len(edges) / max(1, len(nodes)), 4),
    }
