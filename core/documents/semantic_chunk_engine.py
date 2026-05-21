from __future__ import annotations

def build_semantic_chunks(text: str, chunk_size: int = 1200):
    src = text or ""
    chunks = [src[i:i+chunk_size] for i in range(0, len(src), chunk_size)] or [""]
    return {"chunks": chunks, "chunk_ids": [f"chunk_{i:04d}" for i in range(len(chunks))]}
