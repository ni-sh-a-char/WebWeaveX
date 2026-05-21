from __future__ import annotations


def memory_budget(bytes_used: int, limit: int = 1_000_000_000) -> dict:
    used = max(0, int(bytes_used))
    lim = max(1, int(limit))
    return {"ok": used <= lim, "bytes_used": used, "limit": lim}
