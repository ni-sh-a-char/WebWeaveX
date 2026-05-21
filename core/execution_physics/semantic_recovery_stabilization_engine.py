from __future__ import annotations

from typing import Any, Dict


def stabilize_runtime_recovery(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    journal = runtime_ir.get(
        "journal",
        {},
    )

    entries = list(
        journal.get(
            "entries",
            [],
        )
        if isinstance(journal, dict)
        else []
    )

    stabilized = bool(entries)

    return {
        "stabilized": stabilized,
        "stabilization_mode": (
            "journal_replay"
            if stabilized
            else "none"
        ),
    }
