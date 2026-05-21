from __future__ import annotations


def enforce_memory_limit(text: str, max_bytes: int = 5_000_000) -> str:
    raw = (text or "").encode("utf-8", errors="ignore")
    if len(raw) <= max_bytes:
        return text or ""
    return raw[:max_bytes].decode("utf-8", errors="ignore")

