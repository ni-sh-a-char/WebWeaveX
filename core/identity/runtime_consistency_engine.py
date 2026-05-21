from __future__ import annotations

from typing import Any, Dict

from core.identity.browser_entropy_engine import compute_runtime_entropy


def verify_runtime_consistency(
    identity: Dict[str, Any],
    observed: Dict[str, Any],
) -> Dict[str, Any]:
    entropy = compute_runtime_entropy(identity, observed)

    return {
        "consistent": entropy.get("stable", False),
        "entropy": entropy,
        "bounded": True,
    }
