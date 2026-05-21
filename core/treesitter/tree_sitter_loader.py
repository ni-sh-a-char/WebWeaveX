from __future__ import annotations

from typing import Any, Dict

try:
    from tree_sitter import Language
    from tree_sitter import Parser

    TREE_SITTER_AVAILABLE = True

except Exception:

    TREE_SITTER_AVAILABLE = False


SUPPORTED_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "go",
    "rust",
}


def create_parser(
    language: str,
) -> Dict[str, Any]:

    if not TREE_SITTER_AVAILABLE:

        return {
            "available": False,
            "reason": "tree_sitter_missing",
        }

    if language not in SUPPORTED_LANGUAGES:

        return {
            "available": False,
            "reason": "unsupported_language",
        }

    parser = Parser()

    return {
        "available": True,
        "parser": parser,
        "language": language,
    }
