from __future__ import annotations

from typing import Any, Dict, List


def build_justification(
    evidence: List[str],
    lineage: Dict[str, Any],
    uncertainty: Dict[str, Any],
    entropy: Dict[str, Any],
) -> Dict[str, Any]:
    """Expose deterministic justification chain for every cognition object."""
    stages = lineage.get("stages", []) if isinstance(lineage, dict) else []
    steps = [s.get("stage", str(s)) for s in stages if isinstance(s, dict)]
    return {
        "evidence": sorted(set(str(e) for e in evidence if e)),
        "lineage_stages": steps,
        "uncertainty_basis": uncertainty.get("deterministic_inputs", uncertainty.get("factors", [])),
        "entropy": entropy.get("entropy", 0),
        "explainable": True,
        "opaque": False,
        "deterministic_inputs": sorted(
            set(
                [f"evidence_count={len(evidence)}"]
                + [f"stage_count={len(steps)}"]
                + list(uncertainty.get("deterministic_inputs", []) or [])
            )
        ),
    }
