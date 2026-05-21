from __future__ import annotations

import re
from typing import Dict, List

from .symbol_resolution_engine import resolve_symbols


def resolve_api_surface(source: str, language: str, path: str = "") -> Dict[str, object]:
    symbols = resolve_symbols(source, language)
    routes: List[str] = []
    for dec in symbols.get("decorators", []):
        if dec in {"get", "post", "put", "delete", "patch", "route"}:
            routes.append(dec)
    routes.extend(re.findall(r"@(?:app|router)\.(get|post|put|delete|patch)\(['\"]([^'\"]+)", source or ""))
    routes.extend(re.findall(r"\b(?:GET|POST|PUT|DELETE|PATCH)\s+(/[^\s'\"]+)", source or ""))
    graphql = "graphql" in (source or "").lower()
    return {
        "routes": sorted(set(str(r) for r in routes if r)),
        "graphql": graphql,
        "rest": bool(routes),
        "evidence": "parser_symbols_and_patterns",
    }
