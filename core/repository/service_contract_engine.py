from __future__ import annotations

from typing import Any, Dict, List


def extract_service_contracts(services: List[Dict[str, Any]]) -> Dict[str, Any]:
    contracts = []
    for svc in sorted(services, key=lambda s: str(s.get("name", ""))):
        contracts.append(
            {
                "name": svc.get("name"),
                "endpoints": sorted(svc.get("endpoints", []) or []),
                "evidence": sorted(set(svc.get("evidence", []) or [])),
            }
        )
    return {"contracts": contracts, "count": len(contracts), "deterministic": True}
