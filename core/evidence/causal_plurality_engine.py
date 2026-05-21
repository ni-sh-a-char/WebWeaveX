from __future__ import annotations

from typing import Any, Dict, List


def model_causal_plurality(inferred: Dict[str, Any]) -> Dict[str, Any]:
    return {"alternatives": [{"cause": k} for k in list(inferred.keys())[:5]], "preserved": True}
