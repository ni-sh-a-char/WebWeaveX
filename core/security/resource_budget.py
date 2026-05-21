from __future__ import annotations

DEFAULT_BYTE_LIMIT = 50_000_000


def enforce_resource_budget(bytes_used: int, limit: int = DEFAULT_BYTE_LIMIT) -> dict:
    used = max(0, int(bytes_used))
    lim = max(1, int(limit))
    ok = used <= lim
    return {"ok": ok, "allowed": ok, "bytes_used": used, "limit": lim}
