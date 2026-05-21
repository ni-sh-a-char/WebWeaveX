from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


class SemanticGraphDatabase:

    def __init__(self) -> None:

        self.nodes: Dict[
            str,
            Dict[str, Any]
        ] = {}

        self.edges: List[
            Dict[str, Any]
        ] = []

    def insert_node(
        self,
        node: Dict[str, Any],
    ) -> None:

        node_id = node.get("id")

        if not node_id:
            return

        self.nodes[node_id] = node

    def insert_edge(
        self,
        edge: Dict[str, Any],
    ) -> None:

        self.edges.append(edge)

    def query_node(
        self,
        node_id: str,
    ) -> Dict[str, Any]:

        return self.nodes.get(
            node_id,
            {},
        )

    def stats(self) -> Dict[str, Any]:

        return {
            "nodes": len(
                self.nodes
            ),
            "edges": len(
                self.edges
            ),
        }
