from __future__ import annotations

import re
from typing import Any, Dict, List


def parse_javascript_ast(source: str, path: str = "") -> Dict[str, Any]:
    """Structural JS/TS cognition via deterministic patterns; tree-sitter when available."""
    imports: List[Dict[str, str]] = []
    calls: List[Dict[str, str]] = []
    nodes: List[Dict[str, str]] = []

    for match in re.finditer(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]", source):
        imports.append({"module": match.group(1), "kind": "es_import"})
    for match in re.finditer(r"function\s+(\w+)", source):
        nodes.append({"name": match.group(1), "kind": "function"})
    for match in re.finditer(r"class\s+(\w+)", source):
        nodes.append({"name": match.group(1), "kind": "class"})
    for match in re.finditer(r"(\w+)\s*\(", source):
        calls.append({"target": match.group(1), "kind": "call"})

    try:
        from core.parsers.ast_engine import parse_ast

        ts = parse_ast(source, "javascript")
        if ts.get("nodes"):
            nodes = ts.get("nodes", nodes)
    except Exception:
        pass

    return {
        "language": "javascript",
        "path": path,
        "nodes": sorted(nodes, key=lambda item: item["name"])[:5000],
        "imports": sorted(imports, key=lambda item: item["module"])[:2000],
        "calls": sorted(calls, key=lambda item: item["target"])[:5000],
        "bounded": True,
    }
