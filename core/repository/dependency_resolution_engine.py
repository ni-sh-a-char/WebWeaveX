from __future__ import annotations

from typing import Any, Dict, List

from core.repository.runtime_dependency_engine import resolve_runtime_dependencies
from core.parsers.parser_registry import parse_source


def resolve_repository_dependencies(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    return resolve_runtime_dependencies(parsed, source)
