from __future__ import annotations

def redirect_guard(chain: list[str], max_hops: int = 10):
    return {"ok": len(chain or []) <= max_hops}
