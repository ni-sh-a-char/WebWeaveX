from __future__ import annotations

import re
from typing import Any, Dict

from core.parsers.parser_registry import parse_source


def detect_async_runtime(source: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(source, path=path) if source else {}
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    funcs = [str(f) for f in sym.get("functions", []) or []]
    async_funcs = [f for f in funcs if f.startswith("async ") or "async def" in (source or "")]
    await_calls = len(re.findall(r"\bawait\b", source or ""))
    return {
        "async_functions": async_funcs[:50],
        "await_count": await_calls,
        "evidence": ["parser:symbols"] if funcs else (["text:await"] if await_calls else []),
        "parser_backed": bool(funcs),
    }
