from __future__ import annotations

from typing import Any

from core.crypto.kaalka_runtime_engine import (
    compute_deterministic_hash,
    compute_deterministic_hash_payload,
)

compute_kaalka_hash = compute_deterministic_hash
compute_kaalka_hash_payload = compute_deterministic_hash_payload

__all__ = ["compute_kaalka_hash", "compute_kaalka_hash_payload"]
