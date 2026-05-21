from __future__ import annotations

from typing import Any, Dict


def analyze_recovery_causality(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    journal = runtime_ir.get(
        "journal",
        {},
    )

    entries = (
        journal.get("entries", [])
        if isinstance(journal, dict)
        else []
    )

    replayable = bool(entries)

    return {
        "recovery_possible": replayable,
        "recovery_mode": (
            "journal_replay"
            if replayable
            else "none"
        ),
    }
