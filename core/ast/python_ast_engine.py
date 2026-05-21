from __future__ import annotations

import ast
from typing import Any, Dict, List


def _node(node: ast.AST) -> Dict[str, Any]:
    return {
        "type": type(node).__name__,
        "lineno": getattr(node, "lineno", None),
        "end_lineno": getattr(node, "end_lineno", None),
    }


def parse_python_ast(code: str) -> Dict[str, Any]:
    tree = ast.parse(code)

    imports: List[Dict[str, Any]] = []
    functions: List[Dict[str, Any]] = []
    classes: List[Dict[str, Any]] = []
    assignments: List[Dict[str, Any]] = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            imports.append({
                "modules": [n.name for n in node.names],
                "node": _node(node),
            })

        elif isinstance(node, ast.ImportFrom):
            imports.append({
                "module": node.module,
                "names": [n.name for n in node.names],
                "node": _node(node),
            })

        elif isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [a.arg for a in node.args.args],
                "node": _node(node),
            })

        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "bases": [
                    getattr(base, "id", None)
                    for base in node.bases
                ],
                "node": _node(node),
            })

        elif isinstance(node, ast.Assign):
            targets = []
            for t in node.targets:
                if isinstance(t, ast.Name):
                    targets.append(t.id)

            assignments.append({
                "targets": targets,
                "node": _node(node),
            })

    return {
        "language": "python",
        "imports": sorted(imports, key=lambda x: str(x)),
        "functions": sorted(functions, key=lambda x: x["name"]),
        "classes": sorted(classes, key=lambda x: x["name"]),
        "assignments": assignments,
        "ast_grounded": True,
        "bounded": True,
    }
