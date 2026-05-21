from __future__ import annotations

from typing import Any, Dict

from core.repository.api_surface_reasoning_engine import reason_api_surface


def reason_api_contract(spec: Dict[str, Any]) -> Dict[str, Any]:
    surface = reason_api_surface(spec)
    contracts = [
        {"path": p["path"], "method": p["method"], "contract": "http", "evidence": ["openapi:paths"]}
        for p in surface.get("paths", [])
    ]
    return {**surface, "contracts": contracts, "contract_count": len(contracts)}
