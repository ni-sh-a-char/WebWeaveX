from __future__ import annotations

from typing import Any

from core.serialize.deterministic_serializer import dumps_deterministic

try:
    import kaalka  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover
    kaalka = None


def _safe_byte(value: int) -> int:
    return ((value % 256) + 256) % 256


def _derive_time_key(token: bytes, idx: int) -> int:
    if not token:
        return 0
    return token[idx % len(token)]


def kaalka_encrypt_bytes(data: bytes, token: bytes) -> bytes:
    encrypted = []
    ln_mod = len(data) % 251
    for i, n in enumerate(data):
        tk = _derive_time_key(token, i)
        value = ((n ^ tk) + (i * 31) + ln_mod) % 256
        encrypted.append(_safe_byte(value))
    return bytes(encrypted)


def hex_fingerprint(payload: Any, token: str = "webweavex") -> str:
    if isinstance(payload, (str, bytes)):
        raw_text = payload.decode("utf-8", errors="ignore") if isinstance(payload, bytes) else payload
    else:
        raw_text = dumps_deterministic(payload)
    raw = raw_text.encode("utf-8", errors="ignore")
    return kaalka_encrypt_bytes(raw, token.encode("utf-8", errors="ignore")).hex()


fingerprint = hex_fingerprint
fingerprint_v2 = hex_fingerprint
fingerprint_v3 = hex_fingerprint
