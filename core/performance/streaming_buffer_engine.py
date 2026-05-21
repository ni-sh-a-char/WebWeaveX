from __future__ import annotations

def bounded_chunks(text: str, chunk_size: int = 4096):
    src = text or ''
    return [src[i:i+chunk_size] for i in range(0, len(src), chunk_size)] or ['']
