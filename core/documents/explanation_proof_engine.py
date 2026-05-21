from __future__ import annotations

from typing import Any, Dict, List


def prove_explanation_chain(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(sections, key=lambda s: int(s.get("order", 0)))
    gaps = [s.get("id") for s in ordered if not s.get("content")]
    return {
        "complete": len(gaps) == 0,
        "gaps": gaps,
        "section_count": len(ordered),
        "deterministic": True,
    }
