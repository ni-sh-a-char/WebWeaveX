from __future__ import annotations


def query_chunks(streaming_meta: dict):
    return streaming_meta.get("chunk_order", [])

