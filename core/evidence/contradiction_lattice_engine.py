from __future__ import annotations

from typing import Any, Dict, List, Tuple


def build_contradiction_lattice(pairs: List[Any]) -> Dict[str, Any]:
    """Lattice over contradiction pairs: count, depth, pressure."""
    normalized: List[Tuple[str, str]] = []
    for p in pairs or []:
        if isinstance(p, (list, tuple)) and len(p) >= 2:
            normalized.append((str(p[0]), str(p[1])))
    count = len(normalized)
    pressure = round(min(1.0, count * 0.25), 3)
    return {
        "pairs": [list(t) for t in sorted(normalized)],
        "count": count,
        "pressure": pressure,
        "rigor": "lattice_enumeration",
        "deterministic_inputs": [f"pair_count={count}", f"pressure={pressure}"],
    }
