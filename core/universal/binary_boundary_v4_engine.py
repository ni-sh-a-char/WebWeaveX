from __future__ import annotations

def inspect_binary_boundary(payload: bytes | str):
    data = payload.encode('utf-8', errors='ignore') if isinstance(payload, str) else (payload or b'')
    return {"size": len(data), "has_null_byte": 0 in data[:4096]}
