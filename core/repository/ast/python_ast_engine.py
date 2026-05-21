from __future__ import annotations

import ast
from typing import Any, Dict, List


def parse_python_ast(source: str, path: str = "") -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    imports: List[Dict[str, str]] = []
    calls: List[Dict[str, str]] = []

    try:
        tree = ast.parse(source, filename=path or "<python>")
    except SyntaxError as exc:
        return {
            "language": "python",
            "parse_error": str(exc),
            "nodes": [],
            "imports": [],
            "calls": [],
            "bounded": True,
        }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({"module": alias.name, "kind": "import"})
        elif isinstance(node, ast.ImportFrom):
            imports.append({"module": node.module or "", "kind": "import_from"})
        elif isinstance(node, ast.Call):
            func = getattr(node.func, "id", None) or getattr(node.func, "attr", "call")
            calls.append({"target": str(func), "kind": "call"})
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nodes.append({"name": node.name, "kind": type(node).__name__})

    return {
        "language": "python",
        "nodes": sorted(nodes, key=lambda item: item["name"]),
        "imports": sorted(imports, key=lambda item: item["module"]),
        "calls": sorted(calls, key=lambda item: item["target"])[:5000],
        "bounded": True,
    }
