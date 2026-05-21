from __future__ import annotations

from typing import Any, Dict, List


def model_explanatory_self_determination(alternative_count: int) -> Dict[str, Any]:
    return {
        "self_determined": alternative_count > 0,
        "submission_blocked": True,
        "dependency_blocked": True,
    }
