from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.semantic_runtime_graph_engine import build_semantic_runtime_graph


def model_service_orchestration(source: str, path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    graph = build_semantic_runtime_graph(source, path, files)
    return {"orchestration_graph": graph, "service_count": len(graph.get("nodes", [])), "evidence": graph.get("evidence", [])}
