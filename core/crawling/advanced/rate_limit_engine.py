from __future__ import annotations

def within_rate_limit(counter: int, limit: int = 60):
    return counter < limit
