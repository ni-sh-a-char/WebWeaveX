from __future__ import annotations

from typing import Any, Dict


def model_recursive_novelty(depth: int, key_count: int, ambiguity_count: int) -> Dict[str, Any]:
    novelty = round(min(1.0, key_count * 0.12 + ambiguity_count * 0.08 + max(0, 3 - depth) * 0.05), 3)
    return {"novelty": novelty, "preserved": novelty > 0.1, "exhaustion_blocked": True}
