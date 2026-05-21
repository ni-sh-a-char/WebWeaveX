from __future__ import annotations

from typing import Iterator, List


def budgeted_chunks(text: str, chunk_size: int = 50_000) -> List[str]:
    raw = text or ""
    size = max(1024, int(chunk_size))
    return [raw[i : i + size] for i in range(0, len(raw), size)] or [""]
