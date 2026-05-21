from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.repository.ast.go_ast_engine import parse_go_ast
from core.repository.ast.java_ast_engine import parse_java_ast
from core.repository.ast.javascript_ast_engine import parse_javascript_ast
from core.repository.ast.python_ast_engine import parse_python_ast
from core.repository.ast.rust_ast_engine import parse_rust_ast

_PARSERS = {
    "python": parse_python_ast,
    "javascript": parse_javascript_ast,
    "typescript": parse_javascript_ast,
    "go": parse_go_ast,
    "rust": parse_rust_ast,
    "java": parse_java_ast,
}

_EXT = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
}


def analyze_source_ast(source: str, path: str = "", language: str = "") -> Dict[str, Any]:
    lang = language or _EXT.get(Path(path).suffix.lower(), "python")
    parser = _PARSERS.get(lang, parse_python_ast)
    result = parser(source, path=path)
    return {
        **result,
        "call_graph": result.get("calls", []),
        "dependencies": result.get("imports", []),
        "semantic_topology": {
            "nodes": len(result.get("nodes", [])),
            "imports": len(result.get("imports", [])),
            "calls": len(result.get("calls", [])),
        },
        "deterministic": True,
        "bounded": True,
    }
