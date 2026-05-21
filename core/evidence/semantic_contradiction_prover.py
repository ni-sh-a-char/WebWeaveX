from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.contradiction_lattice_engine import build_contradiction_lattice


def prove_contradiction_pressure(pairs: List[Any]) -> Dict[str, Any]:
    lattice = build_contradiction_lattice(pairs)
    return {
        "pressure": lattice["pressure"],
        "count": lattice["count"],
        "proved": lattice["count"] > 0,
        "lattice": lattice,
    }
