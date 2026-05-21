from __future__ import annotations

def within_timeout(elapsed_ms: float, limit_ms: float = 10_000.0):
    return elapsed_ms <= limit_ms
