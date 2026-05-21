from __future__ import annotations

from typing import Any, Dict


def model_epistemic_openness(plurality: Dict[str, Any], decentralization: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "open": plurality.get("preserved", True) and decentralization.get("decentralized", True),
        "anti_closure": True,
        "anti_dogmatism": True,
        "anti_canonicalization": True,
        "interpretive_openness": True,
    }
