from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def detect_evidence_conflicts(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    pairs: List[List[str]] = []
    texts = [str(c.get("text", c.get("claim", ""))) for c in claims or []]
    for i, a in enumerate(texts):
        for b in texts[i + 1 :]:
            if a and b and a != b and ("not " in a.lower()) != ("not " in b.lower()):
                pairs.append([a[:40], b[:40]])
    lattice = build_contradiction_lattice(pairs)
    return {"conflicts": lattice["pairs"], "pressure": lattice["pressure"], "count": lattice["count"]}
