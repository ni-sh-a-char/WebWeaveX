from __future__ import annotations

from typing import Any, Dict

from core.evidence import structure_cognition


_INTENT_MARKERS = {
    "tutorial": ("step", "tutorial", "guide", "how to"),
    "reference": ("api", "reference", "parameter", "returns"),
    "architecture": ("architecture", "design", "component", "system"),
}


def classify_semantic_intent(text: str) -> Dict[str, Any]:
    lower = (text or "").lower()
    scores = {k: sum(1 for m in markers if m in lower) for k, markers in _INTENT_MARKERS.items()}
    best = max(scores.items(), key=lambda x: x[1]) if any(scores.values()) else ("unknown", 0)
    observed = {"markers": scores}
    inferred = {"intent": best[0], "score": best[1]}
    reconciled = inferred
    amb = ["intent_ambiguous"] if sum(1 for v in scores.values() if v > 0) > 1 else []
    return structure_cognition(observed, inferred, reconciled, parsed=None, ambiguities=amb)
