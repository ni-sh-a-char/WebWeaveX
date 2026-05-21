from __future__ import annotations

def recursion_guard(depth: int, limit: int = 6):
    return {"ok": depth <= limit}
