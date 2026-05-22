from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class ExtractionRequest:
    kind: str
    target: str
    authenticated: bool = False
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExtractionResult:
    kind: str
    payload: Dict[str, Any]
    graph_nodes: List[Dict[str, Any]] = field(default_factory=list)
    graph_edges: List[Dict[str, Any]] = field(default_factory=list)
    deterministic_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "payload": self.payload,
            "graph_nodes": self.graph_nodes,
            "graph_edges": self.graph_edges,
            "deterministic_hash": self.deterministic_hash,
            "bounded": True,
        }
