"""Kaalka Encryption Algorithm - Deterministic cryptographic wrapper."""


def kaalka_encrypt(data_bytes: bytes, time_key: int) -> bytes:
    result = []
    length_mod = len(data_bytes) % 251

    for i, n in enumerate(data_bytes):
        tk = (time_key >> (i % 8)) & 0xFF
        val = ((n ^ tk) + (i * 31) + length_mod) % 256
        val = ((val % 256) + 256) % 256
        result.append(val)

    return bytes(result)


def graph_fingerprint(graph):
    """Generate deterministic graph fingerprint."""
    import json

    raw = json.dumps(graph, sort_keys=True).encode()
    return kaalka_encrypt(raw, time_key=123456)