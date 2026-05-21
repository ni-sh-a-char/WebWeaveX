from __future__ import annotations

from typing import Any, Dict

from core.repository.runtime_dependency_engine import resolve_runtime_dependencies
from core.parsers.parser_registry import parse_source


def propagate_runtime_dependencies(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    deps = resolve_runtime_dependencies(parsed, source)
    propagated = [{"dep": d, "depth": 1} for d in deps.get("dependencies", [])[:100]]
    return {"propagated": propagated, "evidence": deps.get("evidence", []), "parser_first": deps.get("parser_first")}
