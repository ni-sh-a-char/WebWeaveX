from __future__ import annotations

from typing import Any, Dict

from core.evidence.speculative_inference_engine import suppress_speculative_inference
from core.repository.topology_self_confirmation_engine import suppress_topology_self_confirmation
from core.repository.recursive_topology_lock_engine import suppress_recursive_topology_lock
from core.repository.civilization_topology_engine import apply_civilization_topology
from core.repository.anti_capture_topology_engine import apply_anti_capture_topology
from core.repository.sovereignty_topology_engine import apply_sovereignty_topology
from core.repository.openness_topology_engine import apply_openness_topology


def suppress_speculative_topology_edge(edge: Dict[str, Any]) -> Dict[str, Any]:
    ev = edge.get("evidence", []) or []
    spec = suppress_speculative_inference("topology_edge", ev, inferred=bool(edge.get("inferred")))
    suppressed = spec.get("suppressed", False)
    reality = {"aligned": bool(ev) and not suppressed, "parser_bounded": bool(ev)}
    base = {
        **edge,
        "reality_alignment": reality,
        "boundary_pressure": {"edge": suppressed or not ev},
        "stability": {"stable": bool(ev), "level": "high" if ev else "low"},
        "supported": {"stated": bool(ev)},
        "unsupported": {"edge": suppressed or not ev, "speculative": spec.get("suppressed", False)},
        "suppressed": {"edge": suppressed, "reason": spec.get("record", {}).get("reason") if spec.get("record") else None},
        "fragility": edge.get("fragility", {"level": "medium" if not ev else "low"}),
        "uncertainty": edge.get("uncertainty", {"visible": not ev}),
        "ambiguity": edge.get("ambiguity", {"visible": False}),
        "confidence_caps": edge.get("confidence_caps", edge.get("confidence_limits", {})),
        "evidence": ev,
        "speculative_suppression": spec.get("record"),
    }
    return apply_openness_topology(
        apply_sovereignty_topology(
            apply_anti_capture_topology(
                apply_civilization_topology(
                    suppress_recursive_topology_lock(suppress_topology_self_confirmation(base))
                )
            )
        )
    )
