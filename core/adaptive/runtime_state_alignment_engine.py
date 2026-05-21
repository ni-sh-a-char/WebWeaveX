from __future__ import annotations

from typing import Any, Dict

from core.adaptive.runtime_reconciliation_engine import reconcile_runtime_state


def align_runtime_state(
    runtimes: Dict[str, Any],
) -> Dict[str, Any]:
    reconciled = reconcile_runtime_state(
        browser_runtime=runtimes.get("browser", {}),
        stream_runtime=runtimes.get("stream", {}),
        interaction_runtime=runtimes.get("interaction", {}),
        extraction_runtime=runtimes.get("extraction", {}),
    )

    return {
        "aligned": reconciled.get("consistent", False),
        "reconciliation": reconciled,
        "bounded": True,
    }
