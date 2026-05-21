from __future__ import annotations

from core.streaming.stream_parser import parse_stream


def incremental_extract(text: str):
    parsed = parse_stream(text)
    return {
        "chunks": [{"id": c["id"], "length": len(c["text"])} for c in parsed["chunks"]],
        "chunk_order": parsed["chunk_order"],
    }

