from __future__ import annotations

from typing import Any, Dict, List

SUPPORTED = frozenset({"python", "javascript", "typescript", "rust", "go", "java", "kotlin", "dart"})


def require_parser_evidence(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Reject semantic claims without parser substrate when language is supported."""
    lang = str(parsed.get("language", "text")).lower()
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    flags = parsed.get("evidence", parsed.get("parser_evidence", {})) or {}
    symbol_count = sum(
        len(sym.get(k, []) or [])
        for k in ("classes", "functions", "imports", "exports", "interfaces")
    )
    applicable = lang in SUPPORTED
    grounded = symbol_count > 0 or bool(flags)
    return {
        "language": lang,
        "applicable": applicable,
        "grounded": grounded if applicable else True,
        "symbol_count": symbol_count,
        "parser_required": applicable,
        "deterministic_inputs": [f"lang={lang}", f"symbols={symbol_count}"],
    }
