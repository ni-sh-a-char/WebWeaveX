from __future__ import annotations

def compute_redundancy(items: list[str]):
    total = len(items or [])
    unique = len(set(items or []))
    return {"total": total, "unique": unique, "redundancy": max(0, total - unique)}
