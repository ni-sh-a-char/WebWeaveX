from __future__ import annotations

from typing import Any, Dict, List


def normalize_symbols(semantic_ast: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw = semantic_ast.get("symbols", [])
    if isinstance(raw, dict):
        items = raw.get("symbols", [])
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("symbol")
        if name:
            normalized.append({**item, "name": name})
    return normalized


def normalize_imports(semantic_ast: Dict[str, Any]) -> List[Dict[str, Any]]:
    direct = semantic_ast.get("imports")
    if isinstance(direct, list):
        return direct
    ast = semantic_ast.get("ast", {})
    if not isinstance(ast, dict):
        return []
    result: List[Dict[str, Any]] = []
    for imp in ast.get("imports", []):
        if not isinstance(imp, dict):
            continue
        if "modules" in imp:
            for module in imp.get("modules", []):
                result.append({"module": module})
        elif imp.get("module"):
            module = imp["module"]
            names = imp.get("names", [])
            if names:
                for name in names:
                    result.append({"module": f"{module}.{name}"})
            else:
                result.append({"module": module})
    return result
