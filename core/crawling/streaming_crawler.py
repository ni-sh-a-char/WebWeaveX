from __future__ import annotations

from core.streaming.chunk_engine import chunk_text


def stream_crawl_text(text: str, chunk_size: int = 4096):
    return chunk_text(text or "", chunk_size=chunk_size)

