from __future__ import annotations

from typing import Any, Dict

from core.repository.execution_dependency_engine import model_execution_dependencies
from core.parsers.parser_registry import parse_source


def trace_runtime(source: str, path: str = "") -> Dict[str, Any]:
    deps = model_execution_dependencies(source, path)
    parsed = parse_source(source, path=path) if source else {}
    return {
        "trace": deps.get("edges", [])[:100],
        "entrypoints": deps.get("entrypoints", []),
        "language": parsed.get("language", "text"),
        "evidence": deps.get("evidence", []),
    }
