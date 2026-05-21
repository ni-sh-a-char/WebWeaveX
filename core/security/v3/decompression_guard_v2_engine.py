from __future__ import annotations


def guard_decompression_ratio_v3(compressed_size: int, expanded_size: int, max_ratio: int = 100):
    compressed = max(1, int(compressed_size))
    ratio = int(expanded_size) / compressed
    return {"allowed": ratio <= max_ratio, "ratio": ratio, "max_ratio": max_ratio}
