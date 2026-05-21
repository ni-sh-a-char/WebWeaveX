from __future__ import annotations

from typing import Dict, Iterator, List, Optional

from .parser_budget_engine import ParserBudget, enforce_budget
from .parser_registry import ParserRegistry


def stream_parse(
    source: str,
    path: str = "",
    language_hint: str = "",
    chunk_lines: int = 500,
    budget: Optional[ParserBudget] = None,
) -> Iterator[Dict[str, object]]:
    bounded = enforce_budget(source, budget)
    lines = bounded.splitlines()
    if not lines:
        yield ParserRegistry.parse("", path=path, language_hint=language_hint, budget=budget)
        return

    chunks: List[str] = []
    for i in range(0, len(lines), max(1, chunk_lines)):
        chunks.append("\n".join(lines[i : i + chunk_lines]))

    for idx, chunk in enumerate(chunks):
        parsed = ParserRegistry.parse(chunk, path=path, language_hint=language_hint, budget=budget)
        parsed["chunk_index"] = idx
        parsed["chunk_count"] = len(chunks)
        yield parsed
