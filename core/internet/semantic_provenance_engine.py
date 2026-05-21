from __future__ import annotations

from typing import Any, Dict

from core.internet.citation_lineage_engine import reconstruct_citation_lineage


def build_semantic_provenance(text: str, url: str = "") -> Dict[str, Any]:
    lineage = reconstruct_citation_lineage(text) if text else {"citations": [], "evidence": []}
    return {
        "url": url,
        "citations": lineage.get("citations", []),
        "lineage": lineage.get("lineage", {}),
        "evidence": lineage.get("evidence", []),
        "deterministic_inputs": [f"citations={len(lineage.get('citations', []))}"],
    }
