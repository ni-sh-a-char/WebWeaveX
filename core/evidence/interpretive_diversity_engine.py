from __future__ import annotations

from typing import Any, Dict, List


def model_interpretive_diversity(evidence: List[str], inferred: Dict[str, Any]) -> Dict[str, Any]:
    interpretations = []
    if evidence:
        interpretations.append({"id": "evidence_backed", "evidence": list(evidence), "limitations": []})
    for k in inferred:
        interpretations.append({
            "id": f"infer:{k}",
            "interpretation": {k: inferred[k]},
            "evidence": list(evidence),
            "limitations": ["inferred"] if k not in evidence else [],
            "contradictions": [],
            "ambiguities": [],
            "plurality": {"rank": "secondary" if len(evidence) < 2 else "primary"},
            "confidence": {"capped": len(evidence) < 2},
        })
    return {"preserved": True, "count": len(interpretations), "interpretations": interpretations[:10]}
