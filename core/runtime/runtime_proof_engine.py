from __future__ import annotations

from typing import Any, Dict, List


def prove_runtime_consistency(
    transitions: List[Dict[str, Any]],
    evidence: List[str],
) -> Dict[str, Any]:
    invalid = [t for t in transitions if not t.get("valid", True)]
    return {
        "valid": len(invalid) == 0,
        "invalid_count": len(invalid),
        "evidence": sorted(set(evidence)),
        "grounded": bool(evidence),
        "deterministic": True,
    }
