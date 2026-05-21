from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def detect_ontology_conflicts(edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    pairs: List[List[str]] = []
    for e in edges or []:
        c = e.get("contradictions", {}) or {}
        for p in c.get("pairs", []):
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                pairs.append([str(p[0]), str(p[1])])
    lattice = build_contradiction_lattice(pairs)
    return {
        "conflicts": lattice["pairs"],
        "pressure": lattice["pressure"],
        "contradiction_pressure": lattice["pressure"],
        "uncertainty": {"visible": lattice["count"] > 0},
    }
