from __future__ import annotations

from core.crypto.kaalka_runtime_engine import normalize_runtime_value

MAX_KEY_BYTES = 4096


def derive_kaalka_key_bytes(key: str) -> bytes:
    normalized = normalize_runtime_value(key)
    return normalized.encode("utf-8")[:MAX_KEY_BYTES]
