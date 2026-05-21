from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def model_ontology_contradiction(edge: Dict[str, Any]) -> Dict[str, Any]:
    pairs = (edge.get("contradictions", {}) or {}).get("pairs", [])
    lattice = build_contradiction_lattice(pairs)
    pressure = lattice["pressure"]
    return {**edge, "contradiction_pressure": pressure, "contradiction_lattice": lattice}
