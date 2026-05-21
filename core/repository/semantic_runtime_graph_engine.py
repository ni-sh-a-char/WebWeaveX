from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.service_runtime_graph_engine import build_service_runtime_graph
from core.repository.execution_dependency_engine import model_execution_dependencies


def build_semantic_runtime_graph(source: str, path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    services = build_service_runtime_graph(source, path, files)
    deps = model_execution_dependencies(source, path)
    return {
        "nodes": services.get("nodes", []),
        "edges": services.get("edges", []) + deps.get("edges", []),
        "evidence": sorted(set(services.get("evidence", []) + deps.get("evidence", []))),
    }
