from __future__ import annotations

def enforce_budgets(pages: int, bytes_used: int, max_pages: int = 100, max_bytes: int = 50_000_000):
    return {"pages_ok": pages <= max_pages, "bytes_ok": bytes_used <= max_bytes}
