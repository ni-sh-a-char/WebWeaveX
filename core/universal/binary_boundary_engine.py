from __future__ import annotations

def detect_binary_boundary(payload: bytes | str):
    data = payload.encode('utf-8', errors='ignore') if isinstance(payload, str) else (payload or b'')
    return {"is_binary": data[:2048].count(0) > 0, "size": len(data)}
