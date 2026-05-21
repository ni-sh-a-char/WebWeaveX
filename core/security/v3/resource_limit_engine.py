from __future__ import annotations


def check_resource_limits_v3(bytes_used: int, memory_used: int, byte_limit: int = 50_000_000, memory_limit: int = 1_000_000_000):
    return {
        "bytes_ok": int(bytes_used) <= int(byte_limit),
        "memory_ok": int(memory_used) <= int(memory_limit),
        "byte_limit": int(byte_limit),
        "memory_limit": int(memory_limit),
    }
