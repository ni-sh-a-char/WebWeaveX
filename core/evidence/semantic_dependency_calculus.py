from __future__ import annotations

from typing import Any, Dict, List


def derive_dependency(from_keys: List[str], to_keys: List[str], evidence: List[str]) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in evidence if e))
    derivable = bool(from_keys) and bool(to_keys) and len(ev) >= 1
    return {
        "derivable": derivable,
        "from": list(from_keys),
        "to": list(to_keys),
        "evidence": ev,
        "rule": "dependency_requires_evidence",
        "deterministic_inputs": [f"evidence={len(ev)}"],
    }
