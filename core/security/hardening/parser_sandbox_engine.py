from __future__ import annotations

def sandbox_text(text: str, max_bytes: int = 5_000_000):
    raw=(text or '').encode('utf-8', errors='ignore')
    return raw[:max_bytes].decode('utf-8', errors='ignore')
