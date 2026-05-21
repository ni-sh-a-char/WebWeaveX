from __future__ import annotations

def chunk_semantic(text: str, chunk_size: int = 1500):
    src = text or ''
    chunks = [src[i:i+chunk_size] for i in range(0, len(src), chunk_size)] or ['']
    return {"chunks": chunks, "order": [f"c{i:04d}" for i in range(len(chunks))]}
