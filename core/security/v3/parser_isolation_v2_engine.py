from __future__ import annotations


def safe_parse_text_v3(text: str, max_chars: int = 5_000_000):
    value = text or ""
    return value[:max_chars]
