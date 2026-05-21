from __future__ import annotations

from typing import Any, Dict, List


def model_fragility(
    evidence: List[str],
    ambiguities: List[str],
    contradiction_count: int = 0,
    parser_density: int = 0,
) -> Dict[str, Any]:
    missing = []
    if len(evidence) < 2:
        missing.append("low_evidence_density")
    if parser_density == 0:
        missing.append("no_parser_grounding")
    pressure = [f"contradiction:{contradiction_count}"] if contradiction_count else []
    if len(evidence) >= 3 and not ambiguities and contradiction_count == 0:
        level = "low"
        cap = 0.85
    elif len(evidence) >= 1:
        level = "medium"
        cap = 0.55
    else:
        level = "high"
        cap = 0.35
    if ambiguities:
        level = "high" if level == "medium" else level
        cap = round(min(cap, 0.45), 3)
    return {
        "level": level,
        "basis": {
            "evidence_count": len(evidence),
            "ambiguity_count": len(ambiguities),
            "parser_density": parser_density,
        },
        "missing_support": sorted(set(missing)),
        "contradiction_pressure": pressure,
        "confidence_limits": {"max_score": cap},
    }
