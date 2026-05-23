"""
WebWeaveX → Kaalka v5 adapter (cross-language contract).

normalize_runtime_value → stable_serialize → UTF-8 → derive_kaalka_time_key → kaalka._proc → base64
"""
from __future__ import annotations

import base64
import hashlib
from typing import Any

from core.crypto.kaalka_v5_proc import (
    KAALKA_FALLBACK_TIME_KEY,
    kaalka_time_key_round_trips,
    kaalka_v5_proc,
)
from core.determinism.normalization import normalize_runtime_value, stable_serialize

KAALKA_ALGORITHM = "webweavex-formula+kaalka@5.0.0"
KAALKA_NPM_VERSION = "5.0.0"
MAX_VALUE_BYTES = 10_000_000


def derive_kaalka_time_key(encryption_key: str) -> str:
    digest = hashlib.sha256(normalize_runtime_value(encryption_key).encode("utf-8")).digest()
    for i in range(len(digest) - 2):
        candidate = f"{digest[i] % 12}:{digest[i + 1] % 60}:{digest[i + 2] % 60}"
        if kaalka_time_key_round_trips(candidate):
            return candidate
    if kaalka_time_key_round_trips(KAALKA_FALLBACK_TIME_KEY):
        return KAALKA_FALLBACK_TIME_KEY
    return "12:34:56"


def compute_deterministic_hash(value: Any) -> str:
    payload = stable_serialize(value)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compute_deterministic_hash_payload(payload: Any) -> str:
    return compute_deterministic_hash(payload)


compute_kaalka_hash = compute_deterministic_hash
compute_kaalka_hash_payload = compute_deterministic_hash_payload


def encrypt_bytes(data: bytes, key: str) -> dict[str, Any]:
    bounded = data[:MAX_VALUE_BYTES]
    time_key = derive_kaalka_time_key(key)
    enc = kaalka_v5_proc(bounded, True, time_key)
    return {
        "encrypted": base64.b64encode(enc).decode("ascii"),
        "algorithm": KAALKA_ALGORITHM,
        "deterministic": True,
        "bounded": True,
    }


def decrypt_bytes(data: bytes, key: str) -> dict[str, Any]:
    time_key = derive_kaalka_time_key(key)
    dec = kaalka_v5_proc(data[:MAX_VALUE_BYTES], False, time_key)
    return {
        "decrypted": dec,
        "algorithm": KAALKA_ALGORITHM,
        "deterministic": True,
        "bounded": True,
    }


def encrypt_value(value: Any, key: str) -> dict[str, Any]:
    payload = stable_serialize(value)
    raw = payload.encode("utf-8")[:MAX_VALUE_BYTES]
    result = encrypt_bytes(raw, key)
    return {
        "encrypted": result["encrypted"],
        "algorithm": KAALKA_ALGORITHM,
        "deterministic": True,
        "bounded": True,
    }


def decrypt_value(ciphertext: str, key: str) -> dict[str, Any]:
    raw = base64.b64decode(ciphertext.encode("ascii"))
    result = decrypt_bytes(raw, key)
    return {
        "decrypted": result["decrypted"].decode("utf-8"),
        "algorithm": KAALKA_ALGORITHM,
        "deterministic": True,
        "bounded": True,
    }
