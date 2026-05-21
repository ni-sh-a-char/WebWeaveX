from __future__ import annotations

from typing import Any, Dict


def build_runtime_recovery_plan(
    runtime_ir: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "recovery_strategy": "replay_journal",
        "deterministic": True,
    }
