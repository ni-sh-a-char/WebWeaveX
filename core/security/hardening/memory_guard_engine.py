from __future__ import annotations

def memory_guard(bytes_used: int, limit: int = 1_000_000_000):
    return {"ok": bytes_used <= limit}
