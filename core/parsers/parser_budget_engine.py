from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParserBudget:
    max_bytes: int = 5_000_000
    max_nodes: int = 100_000
    max_depth: int = 256


def enforce_budget(source: str, budget: ParserBudget | None = None) -> str:
    b = budget or ParserBudget()
    raw = (source or "").encode("utf-8", errors="ignore")
    if len(raw) <= b.max_bytes:
        return source or ""
    return raw[: b.max_bytes].decode("utf-8", errors="ignore")
