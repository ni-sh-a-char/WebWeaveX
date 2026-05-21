from __future__ import annotations

import ast
from typing import Any, Dict, List

MAX_AST_NODES = 100_000


def parse_ast(source: str, language: str) -> Dict[str, Any]:
    lang = (language or "text").lower()
    if lang == "python":
        return _python_ast(source)
    return _tree_sitter_ast(source, lang)


def _python_ast(source: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(source or "")
    except SyntaxError:
        return {"language": "python", "nodes": [], "parse_error": True}
    nodes: List[Dict[str, Any]] = []
    stack: List[ast.AST] = [tree]
    idx = 0
    while stack and idx < MAX_AST_NODES:
        node = stack.pop()
        idx += 1
        nodes.append({"id": idx, "kind": type(node).__name__})
        stack.extend(reversed(list(ast.iter_child_nodes(node))))
    return {"language": "python", "nodes": nodes}


def _tree_sitter_ast(source: str, language: str) -> Dict[str, Any]:
    try:
        from tree_sitter_languages import get_parser  # type: ignore

        parser = get_parser(language)
        tree = parser.parse(bytes(source or "", "utf-8", errors="ignore"))
        nodes: List[Dict[str, Any]] = []
        idx = 0
        stack = [(tree.root_node, 0)]
        while stack and idx < MAX_AST_NODES:
            node, depth = stack.pop()
            idx += 1
            nodes.append({"id": idx, "kind": node.type, "depth": depth})
            for child in reversed(node.children):
                stack.append((child, depth + 1))
        return {"language": language, "nodes": nodes}
    except Exception:
        return {"language": language, "nodes": [], "parse_error": True}
