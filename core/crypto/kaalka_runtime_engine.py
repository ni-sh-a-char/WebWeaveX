from __future__ import annotations

import unicodedata
from typing import Any, Dict

from core.crypto.kaalka_engine import kaalka_encrypt_bytes

MAX_VALUE_BYTES = 10_000_000
MAX_KEY_BYTES = 4096


def normalize_runtime_value(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.rstrip()


def _derive_token(key: str) -> bytes:
    return normalize_runtime_value(key).encode("utf-8")[:MAX_KEY_BYTES]


def _kaalka_decrypt_bytes(data: bytes, token: bytes) -> bytes:
    decrypted = []
    ln_mod = len(data) % 251

    for i, n in enumerate(data):
        tk = token[i % len(token)] if token else 0
        plain = (n - (i * 31) - ln_mod) % 256
        decrypted.append(plain ^ tk)

    return bytes(decrypted)


def encrypt_bytes(data: bytes, key: str) -> Dict[str, Any]:
    bounded = data[:MAX_VALUE_BYTES]
    token = _derive_token(key)
    encrypted = kaalka_encrypt_bytes(bounded, token)

    return {
        "encrypted": encrypted.hex(),
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }


def decrypt_bytes(data: bytes, key: str) -> Dict[str, Any]:
    token = _derive_token(key)
    decrypted = _kaalka_decrypt_bytes(data[:MAX_VALUE_BYTES], token)

    return {
        "decrypted": decrypted,
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }


def encrypt_value(value: str, key: str) -> Dict[str, Any]:
    normalized = normalize_runtime_value(value)
    payload = encrypt_bytes(normalized.encode("utf-8"), key)

    return {
        "encrypted": payload["encrypted"],
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }


def decrypt_value(ciphertext: str, key: str) -> Dict[str, Any]:
    raw = bytes.fromhex(ciphertext)
    result = decrypt_bytes(raw, key)
    decrypted_bytes = result["decrypted"]

    return {
        "decrypted": decrypted_bytes.decode("utf-8", errors="strict"),
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }
