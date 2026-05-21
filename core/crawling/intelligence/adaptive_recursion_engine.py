from __future__ import annotations

def adaptive_recursion(depth: int, edges: int, max_depth: int = 3):
    if edges > 5000:
        max_depth = min(max_depth, 2)
    return {"allowed": depth <= max_depth, "max_depth": max_depth}
