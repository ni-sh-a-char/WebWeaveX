from __future__ import annotations

from typing import Any, Dict, List


LIFECYCLE_PHASES = ("bootstrap", "ready", "serving", "draining", "stopped")


def infer_service_lifecycle(
    services: List[Dict[str, Any]],
    parser_evidence: List[str],
) -> Dict[str, Any]:
    phases = []
    for svc in sorted(services, key=lambda s: str(s.get("name", ""))):
        phase = str(svc.get("phase", "bootstrap")).lower()
        if phase not in LIFECYCLE_PHASES:
            phase = "bootstrap"
        phases.append({"name": svc.get("name"), "phase": phase})
    return {
        "services": phases,
        "evidence": sorted(set(parser_evidence)),
        "grounded": bool(parser_evidence),
        "deterministic": True,
    }
