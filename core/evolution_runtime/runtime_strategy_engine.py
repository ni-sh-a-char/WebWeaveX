from __future__ import annotations

from typing import Any, Dict, Optional


def build_runtime_strategy(
    evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    evidence = evidence or {}
    drift_count = int(evidence.get("drift_count", 0))
    failed_steps = int(evidence.get("failed_steps", 0))

    return {
        "extraction_path": "browser_first" if drift_count == 0 else "repair_then_extract",
        "synchronization_path": "continuous" if failed_steps == 0 else "converge_then_sync",
        "workflow_order": "priority_asc",
        "selector_hierarchy": ["healed", "structural", "fallback"],
        "recovery_order": [
            "heal_selector",
            "recover_workflow",
            "resync_runtime",
        ],
        "bounded": True,
    }
