from __future__ import annotations

from typing import Any, Dict, List, Optional


def repair_runtime_failures(
    failures: Optional[List[str]] = None,
    selectors: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    failures = failures or []
    selectors = selectors or {}
    repairs: List[Dict[str, Any]] = []

    repair_map = {
        "broken_selector": "heal_selector",
        "failed_workflow": "reorder_workflow",
        "sync_divergence": "resync_runtime",
        "runtime_inconsistency": "verify_consistency",
        "causality_gap": "bridge_causality",
    }

    for failure in sorted(failures):
        action = repair_map.get(failure, "retry_step")
        repairs.append({
            "failure": failure,
            "action": action,
            "repaired": True,
        })

    for selector, healed in sorted(selectors.items()):
        repairs.append({
            "failure": "broken_selector",
            "action": "heal_selector",
            "selector": selector,
            "healed": healed,
            "repaired": True,
        })

    return {
        "repairs": repairs,
        "repair_count": len(repairs),
        "bounded": True,
    }
