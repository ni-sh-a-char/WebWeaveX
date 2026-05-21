from __future__ import annotations

from typing import Any, Dict, List


MAX_ENGINEERING_NODES = 10000


def build_semantic_engineering_graph(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    topology = runtime_ir.get(
        "distributed_topology",
        {},
    )

    nodes = list(
        topology.get(
            "nodes",
            [],
        )
    )

    edges = list(
        topology.get(
            "edges",
            [],
        )
    )

    bounded_nodes = nodes[
        :MAX_ENGINEERING_NODES
    ]

    bounded_edges = edges[
        :MAX_ENGINEERING_NODES
    ]

    return {
        "nodes": bounded_nodes,
        "edges": bounded_edges,
        "graph_size": (
            len(bounded_nodes)
            + len(bounded_edges)
        ),
        "bounded": True,
    }
