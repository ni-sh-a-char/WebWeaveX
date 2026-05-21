from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


class SemanticGraphStorage:

    def __init__(self) -> None:

        self.nodes: Dict[
            str,
            Dict[str, Any]
        ] = {}

        self.edges: List[
            Dict[str, Any]
        ] = []

    def add_node(
        self,
        node: Dict[str, Any],
    ) -> None:

        self.nodes[
            node["id"]
        ] = node

    def add_edge(
        self,
        edge: Dict[str, Any],
    ) -> None:

        self.edges.append(edge)

    def snapshot(self) -> Dict[str, Any]:

        return {
            "nodes": list(
                self.nodes.values()
            ),
            "edges": self.edges,
        }
