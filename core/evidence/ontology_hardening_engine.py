from __future__ import annotations

from typing import Any, Dict


def detect_ontology_hardening(depth: int, evidence_count: int) -> Dict[str, Any]:
    hardened = depth >= 3 and evidence_count < 2
    return {
        "hardening_detected": hardened,
        "suppress": hardened,
        "plurality_pressure": {"preserve_alternatives": True},
    }
