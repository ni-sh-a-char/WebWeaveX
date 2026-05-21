from __future__ import annotations

from core.internet.trust_engine import compute_trust


def score_trust(url: str, corroboration_count: int = 0, html_text: str = ""):
    """Explainable trust score — delegates to canonical compute_trust."""
    result = compute_trust(url, corroboration_count=corroboration_count)
    if html_text:
        from core.internet.citation_lineage_engine import reconstruct_citation_lineage

        cites = reconstruct_citation_lineage(html_text)
        result["citation_lineage"] = cites
        result["evidence"] = sorted(set(result.get("evidence", [])) + cites.get("evidence", []))
        result["deterministic_inputs"] = sorted(
            set(result.get("deterministic_inputs", [])) + [f"citations={cites['citation_count']}"]
        )
    return result
