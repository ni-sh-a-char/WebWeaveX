from __future__ import annotations

from typing import Any, Dict, List

from core.ast import compile_semantic_ast_ir
from core.ssa.multilang_ssa_engine import build_multilang_ssa
from .language_registry import detect_language
from .tree_sitter_loader import create_parser
from .universal_ast_normalizer import normalize_ast


def parse_universal_ast(
    source: str,
    path: str,
) -> Dict[str, Any]:

    language = detect_language(path) or "text"
    ts = create_parser(language) if language in {"python", "javascript", "typescript", "go", "rust"} else {"available": False}

    if language == "python":

        ir = compile_semantic_ast_ir(source)

        return {
            "language": language,
            "ir": ir,
            "parser": "python_ast",
            "tree_sitter": ts.get("available", False),
            "grounded": True,
        }

    raw_nodes: List[Dict[str, Any]] = [
        {"type": "source_line", "parent": None}
        for _ in source.splitlines()[:100]
    ]
    normalized = normalize_ast(raw_nodes, language)
    multilang = build_multilang_ssa(source, language)

    return {
        "language": language,
        "ir": {
            "normalized_ast": normalized,
            "multilang_ssa": multilang,
            "unsupported_language": language not in {"javascript", "typescript", "go", "rust", "python"},
        },
        "parser": "tree_sitter" if ts.get("available") else "fallback",
        "tree_sitter": ts.get("available", False),
        "grounded": multilang.get("supported", False),
    }
