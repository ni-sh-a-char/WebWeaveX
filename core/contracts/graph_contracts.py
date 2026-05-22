from __future__ import annotations

from typing import Any, Dict, List


class RuntimeGraphContract:
    """Stable runtime graph shape for merge and replay."""

    @staticmethod
    def normalize(graph: Dict[str, Any]) -> Dict[str, Any]:
        nodes = list(graph.get("nodes", []))
        edges = list(graph.get("edges", []))
        nodes_sorted = sorted(
            nodes,
            key=lambda n: (
                str(n.get("id", "")),
                str(n.get("type", "")),
                str(n.get("name", "")),
            ),
        )
        edges_sorted = sorted(
            edges,
            key=lambda e: (
                str(e.get("source", e.get("from", ""))),
                str(e.get("target", e.get("to", ""))),
                str(e.get("type", "")),
            ),
        )
        return {
            "nodes": nodes_sorted,
            "edges": edges_sorted,
            "bounded": True,
        }
