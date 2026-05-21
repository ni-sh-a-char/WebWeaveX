from __future__ import annotations

from core.extract.pipeline import extract
from core.streaming.incremental_extractor import incremental_extract


def stream_extract(input_data):
    text = input_data if isinstance(input_data, str) else str(input_data)
    inc = incremental_extract(text)
    out = extract(text)
    out["metadata"]["streaming"] = {"chunk_count": len(inc["chunks"]), "chunk_order": inc["chunk_order"]}
    return out

