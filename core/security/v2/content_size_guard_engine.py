from __future__ import annotations
def safe_content_size(size:int, limit:int=50_000_000):
    return size <= limit
