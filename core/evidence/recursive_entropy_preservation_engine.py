from __future__ import annotations

from typing import Any, Dict, List


def preserve_recursive_entropy(ambiguities: List[str], uncertainties: List[str], depth: int) -> Dict[str, Any]:
    entropy = round(min(1.0, len(ambiguities) * 0.1 + len(uncertainties) * 0.08 + depth * 0.02), 3)
    return {"entropy": entropy, "preserved": True, "collapse_blocked": True}
