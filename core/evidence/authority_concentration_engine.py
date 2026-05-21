from __future__ import annotations

from typing import Any, Dict


def detect_authority_concentration(dominant: bool, depth: int) -> Dict[str, Any]:
    concentrated = dominant and depth >= 2
    return {"concentrated": concentrated, "suppress": concentrated, "diffusion_required": concentrated}
