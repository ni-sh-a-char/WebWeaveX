from __future__ import annotations

from typing import Any, Dict, List

from core.runtime.semantic_scheduler_engine import schedule_semantic_runtime_tasks
from core.runtime.runtime_state_machine_engine import RuntimeStateMachine


def orchestrate_semantic_execution(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    schedule = schedule_semantic_runtime_tasks(tasks)
    sm = RuntimeStateMachine()
    sm.transition("scheduled", evidence=["orchestrator"])
    sm.transition("running", evidence=["orchestrator"])
    return {
        "schedule": schedule,
        "runtime_state": sm.state,
        "history_len": len(sm.history),
        "deterministic": True,
    }
