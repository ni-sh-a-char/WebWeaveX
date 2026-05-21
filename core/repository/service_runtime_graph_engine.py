from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.service_interaction_engine import infer_service_interactions
from core.parsers.parser_registry import parse_source


def build_service_runtime_graph(
    source: str,
    path: str = "",
    files: Optional[List[str]] = None,
) -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    interactions = infer_service_interactions(parsed, files or [])
    nodes = sorted({i.get("from") for i in interactions.get("interactions", []) if i.get("from")})
    nodes += sorted({i.get("to") for i in interactions.get("interactions", []) if i.get("to")})
    return {
        "nodes": sorted(set(str(n) for n in nodes if n))[:200],
        "edges": interactions.get("interactions", [])[:200],
        "service_files": interactions.get("service_files", []),
        "evidence": interactions.get("evidence", []),
    }
