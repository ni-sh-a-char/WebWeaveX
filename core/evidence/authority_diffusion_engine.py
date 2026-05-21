from __future__ import annotations

from typing import Any, Dict, List


def diffuse_authority(interpretations: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"diffused": len(interpretations) != 1, "interpretation_count": len(interpretations)}
