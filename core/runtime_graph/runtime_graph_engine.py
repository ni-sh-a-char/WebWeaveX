from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

MAX_GRAPH_NODES = 1_000_000
MAX_GRAPH_EDGES = 5_000_000


def build_runtime_graph(
    runtime_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Merge heterogeneous runtime IRs into one canonical graph.

    Deterministic.
    Bounded.
    Source-preserving.
    """

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    seen_nodes: Set[str] = set()
    seen_edges: Set[Tuple[str, str, str]] = set()

    for runtime in runtime_irs[:10000]:
        runtime_type = str(runtime.get("ir", "unknown"))

        runtime_nodes = list(runtime.get("nodes", []) or [])
        runtime_edges = list(runtime.get("edges", []) or [])

        for node in runtime_nodes:
            node_id = str(node.get("id", "")).strip()

            if not node_id:
                continue

            if node_id in seen_nodes:
                continue

            seen_nodes.add(node_id)

            enriched = dict(node)
            enriched["runtime_type"] = runtime_type

            nodes.append(enriched)

            if len(nodes) >= MAX_GRAPH_NODES:
                break

        for edge in runtime_edges:
            src = str(edge.get("from", "")).strip()
            dst = str(edge.get("to", "")).strip()

            relation = str(
                edge.get("relation", "related_to")
            ).strip()

            if not src or not dst:
                continue

            edge_key = (src, dst, relation)

            if edge_key in seen_edges:
                continue

            seen_edges.add(edge_key)

            enriched = dict(edge)
            enriched["runtime_type"] = runtime_type

            edges.append(enriched)

            if len(edges) >= MAX_GRAPH_EDGES:
                break

    return {
        "ir": "unified_runtime_graph",
        "nodes": sorted(
            nodes,
            key=lambda x: str(x.get("id", "")),
        ),
        "edges": sorted(
            edges,
            key=lambda x: (
                str(x.get("from", "")),
                str(x.get("to", "")),
                str(x.get("relation", "")),
            ),
        ),
        "bounded": True,
    }
