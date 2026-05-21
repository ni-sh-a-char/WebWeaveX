from __future__ import annotations

from typing import Any, Dict

from core.repository.api_surface_reasoning_engine import reason_api_surface
from core.ir._base import empty_lineage

ApiIR = Dict[str, Any]


def compile_api_ir(spec: Dict[str, Any]) -> ApiIR:
    surface = reason_api_surface(spec)
    return {
        "paths": surface.get("paths", []),
        "path_count": surface.get("path_count", 0),
        "evidence": surface.get("evidence", []),
        "lineage": empty_lineage("api_ir"),
        "confidence": {"score": 1.0 if surface.get("path_count") else 0.0, "deterministic": True},
    }
