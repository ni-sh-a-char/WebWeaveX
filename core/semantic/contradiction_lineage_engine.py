from __future__ import annotations

from core.evidence.lineage_engine import build_lineage
from core.evidence.contradiction_evidence_engine import detect_contradiction_evidence


def trace_contradiction_lineage(snippets: list[str]):
    detection = detect_contradiction_evidence(snippets)
    lineage = build_lineage(
        [
            {"stage": "collect_snippets", "inputs": [], "outputs": [f"snippet:{i}" for i in range(len(snippets or []))]},
            {"stage": "detect_polarity", "inputs": ["snippets"], "outputs": [str(p) for p in detection.get("contradiction_pairs", [])]},
        ]
    )
    return {**detection, "lineage": lineage}
