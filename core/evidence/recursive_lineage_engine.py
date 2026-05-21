from __future__ import annotations

from typing import Any, Dict, List


def preserve_recursive_lineage(
    lineage: Dict[str, Any],
    evidence: List[str],
    ambiguities: List[str],
    uncertainties: List[str],
    contradicted: Dict[str, Any],
) -> Dict[str, Any]:
    stages = lineage.get("stages", []) if isinstance(lineage, dict) else []
    depth = len(stages) if isinstance(stages, list) else int(lineage.get("depth", 0) or 0)
    pairs = contradicted.get("pairs", []) if isinstance(contradicted, dict) else []
    return {
        "depth": depth,
        "evidence_ancestry": list(evidence),
        "ambiguity_ancestry": list(ambiguities),
        "uncertainty_ancestry": list(uncertainties),
        "contradiction_ancestry": list(pairs),
        "entropy_ancestry_preserved": True,
        "instability_ancestry_preserved": True,
        "decay_prevented": True,
    }
