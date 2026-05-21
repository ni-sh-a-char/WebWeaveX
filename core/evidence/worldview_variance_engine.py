from __future__ import annotations

from typing import Any, Dict, List


def model_worldview_variance(interpretation_count: int, contradiction_pairs: int) -> Dict[str, Any]:
    variance = round(min(1.0, interpretation_count * 0.2 + contradiction_pairs * 0.15), 3)
    return {"variance": variance, "preserved": variance > 0, "convergence_blocked": True}
