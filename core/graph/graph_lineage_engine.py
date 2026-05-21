from __future__ import annotations

from typing import Any, Dict, List


def build_lineage(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Graph lineage for export pipeline compatibility."""
    nodes = graph.get("nodes", []) or []
    edges = graph.get("edges", []) or []
    stages = [{"stage": "graph", "nodes": len(nodes), "edges": len(edges)}]
    return {"stages": stages, "depth": len(stages), "node_count": len(nodes), "edge_count": len(edges)}


def stamp_graph_lineage(graph: Dict[str, Any], stage: str = "graph") -> Dict[str, Any]:
    lineage = graph.get("lineage", {}) or {}
    stages: List[Dict[str, Any]] = list(lineage.get("stages", [])) if isinstance(lineage.get("stages"), list) else []
    stages.append({"stage": stage, "nodes": len(graph.get("nodes", [])), "edges": len(graph.get("edges", []))})
    return {**graph, "lineage": {**lineage, "stages": stages, "depth": len(stages)}}
