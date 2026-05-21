from __future__ import annotations

from typing import Dict, List, Set, Tuple


def detect_contradiction_evidence(snippets: List[str]) -> Dict[str, object]:
    normalized: Dict[str, Set[int]] = {}
    for idx, text in enumerate(snippets or []):
        lower = (text or "").lower()
        for token in ("true", "false", "enabled", "disabled", "deprecated", "stable"):
            if token in lower:
                normalized.setdefault(token, set()).add(idx)
    pairs: List[Tuple[str, str]] = []
    conflicts: List[Dict[str, object]] = []
    opposites = (("true", "false"), ("enabled", "disabled"), ("deprecated", "stable"))
    for a, b in opposites:
        if a in normalized and b in normalized:
            pairs.append((a, b))
            conflicts.append(
                {
                    "polarity_a": a,
                    "polarity_b": b,
                    "snippet_indices_a": sorted(normalized[a]),
                    "snippet_indices_b": sorted(normalized[b]),
                    "evidence": "polarity_conflict",
                }
            )
    return {
        "contradiction_pairs": pairs,
        "conflicts": conflicts,
        "evidence": ["deterministic_polarity_scan"],
        "sources": [f"snippet:{i}" for i in sorted({i for s in normalized.values() for i in s})],
        "grounding": {"method": "polarity_token_scan"},
        "lineage": {"stage": "contradiction_evidence"},
        "confidence_basis": {"conflict_count": len(conflicts)},
    }
