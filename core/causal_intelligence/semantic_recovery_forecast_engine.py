from __future__ import annotations

from typing import Any, Dict


def forecast_recovery_outcome(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:
    recovery = runtime_ir.get("recovery_causality", {})
    if not isinstance(recovery, dict):
        recovery = analyze_recovery_inline(runtime_ir)
    possible = recovery.get("recovery_possible", False)
    return {
        "recovery_forecast": (
            "successful"
            if possible
            else "unavailable"
        ),
        "deterministic": True,
    }


def analyze_recovery_inline(runtime_ir: Dict[str, Any]) -> Dict[str, Any]:
    journal = runtime_ir.get("journal", {})
    entries = (
        journal.get("entries", [])
        if isinstance(journal, dict)
        else []
    )
    return {"recovery_possible": bool(entries)}
