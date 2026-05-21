from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.semantic_incompleteness_engine import model_incompleteness


def preserve_incompleteness(bundle: Dict[str, Any]) -> Dict[str, Any]:
    known = {
        "observed": bundle.get("observed", {}),
        "parsed": bundle.get("parsed", {}),
        "reconciled": bundle.get("reconciled", {}),
    }
    unknown = []
    unsupported = []
    if not bundle.get("evidence"):
        unsupported.append("no_evidence")
    if bundle.get("ambiguities"):
        unknown.extend(bundle.get("ambiguities", []))
    contradicted = bundle.get("contradicted", {}) or {}
    if contradicted.get("preserved") or contradicted.get("pairs"):
        unknown.append("unresolved_contradiction")
    incomplete = model_incompleteness(known, unknown, unsupported)
    return {
        "known": incomplete["known"],
        "unknown": incomplete["unknown"],
        "unsupported": incomplete["unsupported"],
        "ambiguous": bundle.get("ambiguities", []),
        "contradicted": contradicted,
        "incomplete": incomplete["incomplete"],
    }
