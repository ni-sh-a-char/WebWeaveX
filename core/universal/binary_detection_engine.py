from __future__ import annotations
def is_binary(data:bytes):
    return b"\x00" in (data or b"")
