from __future__ import annotations

from typing import Any, Dict, List


def model_explanatory_divergence(alternatives: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"divergence": len(alternatives), "preserved": len(alternatives) > 0, "fixation_blocked": len(alternatives) > 1}
