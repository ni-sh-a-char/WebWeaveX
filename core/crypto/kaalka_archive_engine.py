from __future__ import annotations

import json
from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload
from core.crypto.kaalka_runtime_engine import (
    decrypt_value,
    encrypt_value,
)

MAX_ARCHIVE_BYTES = 50_000_000


def encrypt_extraction_archive(
    data: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    serialized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )[:MAX_ARCHIVE_BYTES]

    encrypted = encrypt_value(serialized, key)
    content_hash = compute_kaalka_hash_payload(data)

    return {
        **encrypted,
        "payload_type": "extraction_archive",
        "content_hash": content_hash,
        "bounded": True,
    }


def decrypt_extraction_archive(
    payload: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    ciphertext = str(payload.get("encrypted", ""))

    decrypted = decrypt_value(ciphertext, key)
    text = str(decrypted.get("decrypted", ""))

    archive = json.loads(text[:MAX_ARCHIVE_BYTES])
    content_hash = compute_kaalka_hash_payload(archive)

    return {
        "archive": archive,
        "content_hash": content_hash,
        "algorithm": "kaalka",
        "deterministic": True,
        "bounded": True,
    }
