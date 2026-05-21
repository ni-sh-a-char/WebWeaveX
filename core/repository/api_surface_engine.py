from __future__ import annotations

from typing import Dict

from core.parsers.api_resolution_engine import resolve_api_surface
from core.parsers.parser_registry import ParserRegistry


def extract_api_surface(text: str, path: str = "") -> Dict[str, object]:
    language = ParserRegistry.detect_language(path=path)
    api = resolve_api_surface(text or "", language, path=path)
    return {
        "routes": api.get("routes", []),
        "rest": api.get("rest", False),
        "graphql": api.get("graphql", False),
        "evidence": api.get("evidence", "parser_api_surface"),
    }
