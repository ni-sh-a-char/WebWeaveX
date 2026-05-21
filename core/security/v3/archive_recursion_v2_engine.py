from __future__ import annotations


def guard_archive_recursion_v3(depth: int, max_depth: int = 5):
    return {"allowed": int(depth) <= int(max_depth), "depth": int(depth), "max_depth": int(max_depth)}
