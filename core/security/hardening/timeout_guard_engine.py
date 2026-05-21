from __future__ import annotations

def timeout_guard(elapsed_ms: float, limit_ms: float = 10_000.0):
    return {"ok": elapsed_ms <= limit_ms}
