from __future__ import annotations

from core.parsers import parse_source


def normalize_ast(text: str, path: str = ""):
    parsed = parse_source(text or "", path=path)
    ast_data = parsed.get("ast", {})
    symbols = parsed.get("symbols", {})
    return {
        "language": parsed.get("language", "text"),
        "ast": ast_data,
        "symbols": symbols,
    }
