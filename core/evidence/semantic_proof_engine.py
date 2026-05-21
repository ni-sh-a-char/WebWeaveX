from __future__ import annotations

from typing import Any, Dict, List


def prove_semantic_claim(
    claim: str,
    evidence: List[str],
    min_evidence: int = 1,
) -> Dict[str, Any]:
    ev = sorted(set(str(e) for e in evidence if e))
    proved = len(ev) >= min_evidence
    return {
        "claim": claim,
        "proved": proved,
        "evidence": ev,
        "steps": [{"rule": "evidence_threshold", "met": proved}],
        "deterministic_inputs": [f"evidence={len(ev)}", f"min={min_evidence}"],
    }
