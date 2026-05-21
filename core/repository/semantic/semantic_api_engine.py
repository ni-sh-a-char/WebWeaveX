from __future__ import annotations

import re
from typing import Dict, List


def reconstruct_semantic_api(text: str) -> Dict[str, List[str]]:
    source = text or ""
    routes = set()
    methods = set()
    handlers = set()

    for m in re.finditer(r"@(app|router)\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]", source):
        methods.add(m.group(2).upper())
        routes.add(m.group(3))

    for m in re.finditer(r"\b(app|router)\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", source):
        methods.add(m.group(2).upper())
        routes.add(m.group(3))
        handlers.add(m.group(4))

    for m in re.finditer(r"\b(function|def|fun)\s+([A-Za-z_][A-Za-z0-9_]*)", source):
        handlers.add(m.group(2))

    return {
        "routes": sorted(routes),
        "methods": sorted(methods),
        "handlers": sorted(handlers),
    }
