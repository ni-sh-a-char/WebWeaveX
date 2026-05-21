from __future__ import annotations

from typing import Any, Dict, List


def apply_confidence_caps(
    score: float,
    fragility: Dict[str, Any],
    contradiction_count: int = 0,
    ambiguity_count: int = 0,
    unsupported_expansion_count: int = 0,
) -> Dict[str, Any]:
    cap = float(fragility.get("confidence_limits", {}).get("max_score", 0.85))
    frag_penalty = {"high": 0.25, "medium": 0.12, "low": 0.0}.get(fragility.get("level", "medium"), 0.12)
    contradict_penalty = round(min(0.35, contradiction_count * 0.12), 3)
    ambig_penalty = round(min(0.25, ambiguity_count * 0.08), 3)
    expand_penalty = round(min(0.2, unsupported_expansion_count * 0.1), 3)
    final = round(max(0.0, min(score, cap) - frag_penalty - contradict_penalty - ambig_penalty - expand_penalty), 3)
    return {
        "score": final,
        "caps": {"fragility_max": cap},
        "fragility_penalties": {"amount": frag_penalty, "level": fragility.get("level")},
        "contradiction_penalties": {"amount": contradict_penalty, "count": contradiction_count},
        "ambiguity_penalties": {"amount": ambig_penalty, "count": ambiguity_count},
        "unsupported_expansion_penalties": {"amount": expand_penalty, "count": unsupported_expansion_count},
        "deterministic_inputs": [
            f"cap={cap}",
            f"contradict={contradiction_count}",
            f"ambig={ambiguity_count}",
            f"expand={unsupported_expansion_count}",
        ],
    }
