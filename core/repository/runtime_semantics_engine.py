from __future__ import annotations

from typing import Any, Dict, Optional

from core.parsers.parser_registry import parse_source
from core.repository.runtime_dependency_engine import resolve_runtime_dependencies


def analyze_runtime_semantics(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    deps = resolve_runtime_dependencies(parsed, source)
    runtime = parsed.get("runtime", {}) if parsed else {}
    return {
        "dependencies": deps["dependencies"],
        "runtime": runtime,
        "parser_first": deps.get("parser_first", False),
        "evidence": deps.get("evidence", []),
        "deterministic_inputs": parsed.get("parser_grounding", {}).get("deterministic_inputs", []),
    }
