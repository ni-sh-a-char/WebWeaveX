from __future__ import annotations

import hashlib
import json
from typing import Any

from core.crypto.kaalka_runtime_engine import normalize_runtime_value

MAX_HASH_INPUT_BYTES = 10_000_000


def compute_kaalka_hash(value: str) -> str:
    normalized = normalize_runtime_value(value)
    digest = hashlib.sha256(
        normalized.encode("utf-8")[:MAX_HASH_INPUT_BYTES]
    )
    return digest.hexdigest()


def compute_kaalka_hash_payload(payload: Any) -> str:
    serialized = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return compute_kaalka_hash(serialized)
