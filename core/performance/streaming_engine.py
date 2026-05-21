from __future__ import annotations


def stream_parse(text: str) -> list:
    raw = text or ""
    return [raw[i : i + 50_000] for i in range(0, max(1, len(raw)), 50_000)] or [""]


def incremental_parse(text: str) -> dict:
    chunks = stream_parse(text)
    return {"segments": chunks}


def lazy_extract(text: str, fields=None) -> dict:
    raw = text or ""
    return {"length": len(raw), "preview": raw[:200]}


def parser_pool() -> dict:
    return {"size": 1, "deterministic": True}
