from __future__ import annotations

from typing import Any, Dict

from core.agents.graph_query_engine import query_edges, query_nodes
from core.ir.semantic_graph_ir import compile_semantic_graph_ir


def query_graph(graph: Dict[str, Any], node: str = "") -> Dict[str, Any]:
    ir = compile_semantic_graph_ir(graph)
    return {
        "ir": ir,
        "nodes": query_nodes(graph, node=node),
        "edges": query_edges(graph, node=node),
        "explainable": True,
        "bounded": True,
    }
