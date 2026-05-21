from __future__ import annotations

from typing import Any, Dict, List

from core.crypto.kaalka_hash_engine import compute_kaalka_hash

PROFILE_IDS = (
    "default",
    "profile_a",
    "profile_b",
)


def build_browser_profile(profile_id: str = "default") -> Dict[str, Any]:
    bounded_id = profile_id if profile_id in PROFILE_IDS else "default"
    seed = compute_kaalka_hash(bounded_id)

    return {
        "profile_id": bounded_id,
        "profile_seed": seed,
        "rotation_index": 0,
        "bounded": True,
    }
