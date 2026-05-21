from __future__ import annotations

from typing import Any, Dict

from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload


def compute_runtime_entropy(
    identity: Dict[str, Any],
    observed: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    baseline = compute_kaalka_hash_payload(
        normalize_browser_fingerprint(identity)
    )

    if not observed:
        return {
            "entropy_score": 0.0,
            "stable": True,
            "baseline_hash": baseline,
            "bounded": True,
        }

    observed_hash = compute_kaalka_hash_payload(
        normalize_browser_fingerprint(observed)
    )

    drift = 0.0 if observed_hash == baseline else 1.0

    return {
        "entropy_score": drift,
        "stable": drift == 0.0,
        "baseline_hash": baseline,
        "observed_hash": observed_hash,
        "bounded": True,
    }


def normalize_browser_fingerprint(
    identity: Dict[str, Any],
) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}

    for key in sorted(identity.keys()):
        if key == "bounded":
            continue

        value = identity[key]

        if isinstance(value, dict):
            normalized[key] = {
                str(k).lower(): value[k]
                for k in sorted(value.keys())
            }
        elif isinstance(value, list):
            normalized[key] = sorted(str(item).lower() for item in value)
        else:
            normalized[key] = str(value).strip().lower()

    return normalized
