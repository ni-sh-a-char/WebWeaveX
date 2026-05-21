from __future__ import annotations

from typing import Any, Dict, List


def model_ontology_boundaries(evidence: List[str], inferred: bool = False) -> Dict[str, Any]:
    allowed = len(evidence) >= 2 and not inferred
    return {
        "expansion_allowed": allowed,
        "inheritance_allowed": allowed,
        "equivalence_allowed": allowed,
        "merge_allowed": len(evidence) >= 3,
    }
