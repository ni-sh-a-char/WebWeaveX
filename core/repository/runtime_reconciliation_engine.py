from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_reconciliation_memory import reconcile_memory_states


def reconcile_runtime_states(states: list) -> Dict[str, Any]:
    return reconcile_memory_states(states)
