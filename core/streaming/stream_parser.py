from __future__ import annotations

from core.streaming.chunk_engine import chunk_text
from core.streaming.memory_guard import enforce_memory_limit


def parse_stream(text: str, chunk_size: int = 4096):
    safe = enforce_memory_limit(text)
    return chunk_text(safe, chunk_size=chunk_size)

