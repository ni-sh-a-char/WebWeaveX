from __future__ import annotations

from typing import Any, Dict, List


class SemanticExecutionGraph:
    def __init__(self, max_nodes: int = 500) -> None:
        self.max_nodes = max_nodes
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, kind: str, metadata: Dict[str, Any] | None = None) -> bool:
        if len(self.nodes) >= self.max_nodes:
            return False
        self.nodes.append({"id": node_id, "kind": kind, "metadata": metadata or {}})
        return True

    def add_edge(self, fr: str, to: str, evidence: List[str] | None = None) -> bool:
        if len(self.edges) >= self.max_nodes:
            return False
        self.edges.append({"from": fr, "to": to, "evidence": evidence or [], "metadata": {}})
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {"nodes": self.nodes, "edges": self.edges, "bounded": len(self.nodes) <= self.max_nodes}
