from __future__ import annotations

def decompression_guard(compressed: int, expanded: int, ratio_limit: int = 100):
    ratio=expanded/max(1,compressed)
    return {"ok": ratio <= ratio_limit, "ratio": ratio}
