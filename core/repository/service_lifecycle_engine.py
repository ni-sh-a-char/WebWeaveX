from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.service_runtime_graph_engine import build_service_runtime_graph


def model_service_lifecycle(source: str, path: str = "", files: Optional[List[str]] = None) -> Dict[str, Any]:
    g = build_service_runtime_graph(source, path, files)
    lifecycle = [{"service": n, "phase": "running"} for n in g.get("nodes", [])[:50]]
    return {"lifecycle": lifecycle, "evidence": g.get("evidence", [])}
