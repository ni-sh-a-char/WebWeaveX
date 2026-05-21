from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.parsers.parser_registry import parse_source
from core.repository.runtime_dependency_engine import resolve_runtime_dependencies
from core.repository.execution_flow_engine import reconstruct_execution_flow
from core.repository.service_interaction_engine import infer_service_interactions


def build_repository_semantic_ir(
    source: str,
    path: str = "",
    files: Optional[List[str]] = None,
) -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    return {
        "language": parsed.get("language", "text"),
        "symbols": parsed.get("symbols", {}),
        "runtime_dependencies": resolve_runtime_dependencies(parsed, source),
        "execution_flow": reconstruct_execution_flow(parsed),
        "service_interactions": infer_service_interactions(parsed, files or []),
        "parser_grounding": parsed.get("parser_grounding", {}),
        "evidence": parsed.get("parser_grounding", {}).get("deterministic_inputs", []),
    }
