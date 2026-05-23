"""Kaalka npm v5.0.0 byte _proc — deterministic clock tuple transform."""
from __future__ import annotations

KAALKA_FALLBACK_TIME_KEY = "12:0:0"
_ROUNDTRIP_PROBE = "\x00\x7f\xff🚀probe".encode("utf-8")


def parse_time_key(time_key: str) -> tuple[int, int, int]:
    parts = str(time_key).split(":")
    h = m = s = 0
    if len(parts) == 3:
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
    elif len(parts) == 2:
        m, s = int(parts[0]), int(parts[1])
    elif len(parts) == 1 and parts[0]:
        s = int(parts[0])
    return h % 12, m, s


def kaalka_v5_proc(data: bytes, encrypt: bool, time_key: str) -> bytes:
    h, m, s = parse_time_key(time_key)
    clock = (h * 3600 + m * 60 + s) or 1
    out = bytearray(len(data))
    for idx, byte in enumerate(data):
        offset = (clock + idx) % 256
        if encrypt:
            out[idx] = (byte + offset) % 256
        else:
            out[idx] = (byte - offset + 256) % 256
    return bytes(out)


def kaalka_time_key_round_trips(time_key: str) -> bool:
    try:
        enc = kaalka_v5_proc(_ROUNDTRIP_PROBE, True, time_key)
        dec = kaalka_v5_proc(enc, False, time_key)
        return dec == _ROUNDTRIP_PROBE
    except (ValueError, TypeError):
        return False
