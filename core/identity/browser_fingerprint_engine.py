from __future__ import annotations

from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload
from core.identity.browser_entropy_engine import normalize_browser_fingerprint


def fingerprint_browser_identity(
    identity: Dict[str, Any],
) -> str:
    return compute_kaalka_hash_payload(
        normalize_browser_fingerprint(identity)
    )
