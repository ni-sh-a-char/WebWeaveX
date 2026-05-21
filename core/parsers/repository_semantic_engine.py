from __future__ import annotations

from typing import Any, Dict

from .parser_registry import ParserRegistry
from .framework_resolution_engine import resolve_frameworks
from .api_resolution_engine import resolve_api_surface
from .semantic_graph_engine import build_semantic_graph


def analyze_repository_source(source: str, path: str = "") -> Dict[str, Any]:
    parsed = ParserRegistry.parse(source, path=path)
    symbols = parsed.get("symbols", {})
    deps = parsed.get("dependencies", {}).get("dependencies", [])
    imports = symbols.get("imports", [])
    frameworks = resolve_frameworks(deps, imports, symbols.get("decorators"))
    api = resolve_api_surface(source, str(parsed.get("language", "text")), path=path)
    parsed["frameworks"] = frameworks
    parsed["api_surface"] = api
    parsed["repository_graph"] = build_semantic_graph(parsed)
    return parsed
