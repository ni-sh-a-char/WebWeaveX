from __future__ import annotations

import hashlib


def extract_binary_metadata(payload: bytes | str):
    data = payload.encode("utf-8", errors="ignore") if isinstance(payload, str) else (payload or b"")
    return {
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "magic_hex": data[:8].hex(),
        "is_binary": any(b == 0 for b in data[:1024]),
    }
