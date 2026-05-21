from __future__ import annotations

from typing import Dict, List


def resolve_semantic_symbols(ast_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    data = ast_data or {}
    resolved = {
        "classes": sorted(set(data.get("classes", []))),
        "interfaces": sorted(set(data.get("interfaces", []))),
        "traits": sorted(set(data.get("traits", []))),
        "functions": sorted(set(data.get("functions", []))),
        "methods": sorted(set(data.get("methods", []))),
        "imports": sorted(set(data.get("imports", []))),
        "exports": sorted(set(data.get("exports", []))),
        "symbols": sorted(set(data.get("symbols", []))),
    }
    resolved["services"] = [s for s in resolved["symbols"] if s.lower().endswith(("service", "controller", "handler"))]
    return resolved
