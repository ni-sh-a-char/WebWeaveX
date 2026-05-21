from __future__ import annotations


def inspect_binary_payload_v3(data: bytes | str, max_size: int = 50_000_000):
    payload = data.encode("utf-8", errors="ignore") if isinstance(data, str) else (data or b"")
    return {"allowed": len(payload) <= max_size, "size": len(payload)}
