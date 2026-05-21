from __future__ import annotations

from typing import Any, Dict, List, Optional


RECOVERY_ACTIONS = {
    "selector_drift": "heal_selector",
    "modal_interruption": "recover_modal",
    "pagination_failure": "retry_pagination",
    "runtime_mutation": "realign_runtime",
    "authentication_expiration": "reauthenticate",
    "worker_failure": "redispatch_worker",
}


def recover_workflow_runtime(
    state: Dict[str, Any],
    failures: Optional[List[str]] = None,
) -> Dict[str, Any]:
    failures = failures or []
    recovered_steps: List[Dict[str, Any]] = []

    for failure in failures[:100]:
        recovered_steps.append({
            "failure": failure,
            "action": RECOVERY_ACTIONS.get(failure, "retry_step"),
            "recovered": True,
        })

    if not failures and state.get("current_step", 0) > 0:
        recovered_steps.append({
            "failure": "implicit_retry",
            "action": "retry_step",
            "recovered": True,
        })

    return {
        "state": {
            **state,
            "retries": int(state.get("retries", 0)) + len(recovered_steps),
        },
        "recovered_steps": recovered_steps,
        "recovered": True,
        "bounded": True,
    }
