from __future__ import annotations

def recursion_guard_v3(depth: int, max_depth: int = 3):
    return {"allowed": int(depth) <= int(max_depth), "depth": int(depth), "max_depth": int(max_depth)}
