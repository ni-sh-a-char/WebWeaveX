from __future__ import annotations

from typing import Dict, Set

SUPPORTED = frozenset(
    {"python", "javascript", "typescript", "java", "kotlin", "dart", "rust", "go"}
)

_CAPABILITIES: Dict[str, Set[str]] = {
    "python": {"ast", "symbols", "imports", "calls", "decorators", "generics"},
    "javascript": {"tree_sitter", "symbols", "imports", "calls"},
    "typescript": {"tree_sitter", "symbols", "imports", "calls", "interfaces", "generics"},
    "java": {"tree_sitter", "symbols", "imports", "annotations"},
    "kotlin": {"tree_sitter", "symbols", "imports", "annotations"},
    "dart": {"tree_sitter", "symbols", "imports"},
    "rust": {"tree_sitter", "symbols", "imports", "traits"},
    "go": {"tree_sitter", "symbols", "imports"},
}


def language_capabilities(language: str) -> Dict[str, object]:
    lang = (language or "text").lower()
    caps = _CAPABILITIES.get(lang, set())
    return {
        "language": lang,
        "supported": lang in SUPPORTED,
        "capabilities": sorted(caps),
        "parser_backend": "native_ast" if lang == "python" else "tree_sitter",
    }
