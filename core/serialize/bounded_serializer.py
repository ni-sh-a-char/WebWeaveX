from __future__ import annotations

from typing import Any

from .deterministic_serializer import dumps_deterministic

MAX_SERIALIZE_BYTES = 50_000_000


def dumps_bounded(value: Any, max_bytes: int = MAX_SERIALIZE_BYTES) -> str:
    out = dumps_deterministic(value)
    raw = out.encode("utf-8", errors="ignore")
    if len(raw) <= max_bytes:
        return out
    return raw[:max_bytes].decode("utf-8", errors="ignore")
