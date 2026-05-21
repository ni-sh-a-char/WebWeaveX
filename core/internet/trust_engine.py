from __future__ import annotations

from typing import Dict, List, Optional

from core.evidence.epistemic_confidence_engine import score_epistemic_confidence
from core.evidence.semantic_confidence_engine import score_semantic_confidence
from core.internet.authority_engine import score_authority
from core.internet.citation_lineage_engine import reconstruct_citation_lineage
from core.internet.semantic_consistency_engine import analyze_semantic_consistency
from core.semantic.contradiction_preservation_engine import preserve_contradictions


def compute_trust(
    url: str,
    corroboration_count: int = 0,
    html_text: str = "",
    claims: Optional[List[Dict[str, object]]] = None,
) -> Dict[str, object]:
    authority = score_authority(url)
    contradictions = preserve_contradictions([html_text[:500]] if html_text else [])
    extra = list(authority.get("evidence", [])) + [f"corroboration:{corroboration_count}"]
    confidence = score_semantic_confidence(extra_evidence=extra)
    epistemic = score_epistemic_confidence(
        evidence=extra,
        uncertainty_factors=["contradiction"] if contradictions.get("contradicted", {}).get("preserved") else [],
        parser_density=0,
    )
    corroboration = {"count": corroboration_count, "evidence": [f"corroboration:{corroboration_count}"]}
    semantic_agreement = analyze_semantic_consistency(claims or [])
    citation_lineage = reconstruct_citation_lineage(html_text) if html_text else {"citations": [], "evidence": []}
    score = round(min(1.0, epistemic["score"] * 0.5 + authority["authority_score"] * 0.35 + min(0.15, corroboration_count * 0.05)), 3)
    if contradictions.get("contradicted", {}).get("preserved"):
        score = round(min(score, 0.5), 3)
    deterministic_inputs = sorted(
        set(confidence.get("deterministic_inputs", []))
        | set(authority.get("deterministic_inputs", []))
        | {f"corroboration={corroboration_count}", f"citations={citation_lineage.get('citation_count', 0)}"}
    )
    return {
        "url": url,
        "trust_score": score,
        "authority": authority,
        "score": score,
        "basis": {
            "authority": authority["authority_score"],
            "corroboration": corroboration_count,
            "citation_count": citation_lineage.get("citation_count", 0),
            **confidence.get("basis", {}),
        },
        "evidence": sorted(
            set(list(authority.get("evidence", [])) + list(confidence.get("evidence", [])) + citation_lineage.get("evidence", []))
        ),
        "deterministic_inputs": deterministic_inputs,
        "contradictions": contradictions.get("contradicted", {}),
        "corroboration": corroboration,
        "semantic_agreement": semantic_agreement.get("semantic_agreement", {}),
        "lineage": {"stage": "trust_scoring", "citation_lineage": citation_lineage.get("lineage", {})},
        "confidence_basis": epistemic,
        "supporting_evidence": epistemic.get("supporting_evidence", []),
        "contradicting_evidence": epistemic.get("contradicting_evidence", []),
        "uncertainty_factors": epistemic.get("uncertainty_factors", []),
        "sources": [url] if url else [],
        "grounding": {"method": "authority_corroboration_citation"},
    }


def rank_trust(urls: List[str]) -> List[Dict[str, object]]:
    return sorted([compute_trust(u) for u in urls or []], key=lambda x: (-x["trust_score"], x["url"]))
