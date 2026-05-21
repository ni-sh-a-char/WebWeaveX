from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.evidence_algebra_engine import combine_evidence
from core.evidence.evidence_weighting_calculus import weight_evidence_calculus


def resolve_evidence(evidence: List[str], parser_backed: bool = False) -> Dict[str, Any]:
    algebra = combine_evidence(evidence)
    weights = weight_evidence_calculus(evidence, parser_backed)
    resolved = algebra["items"] if algebra["sufficient"] else algebra["items"][:1]
    return {
        "resolved": resolved,
        "sufficient": algebra["sufficient"],
        "weights": weights["weights"],
        "deterministic_inputs": algebra["deterministic_inputs"] + weights["deterministic_inputs"],
    }
