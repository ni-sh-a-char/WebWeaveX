from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.execution.runtime_execution_engine import execute_runtime_action
from core.execution.runtime_mutation_engine import track_runtime_mutations
from core.execution.runtime_sandbox_engine import build_runtime_sandbox


def simulate_runtime_execution(
    actions: List[Dict[str, Any]],
    sandbox: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    sandbox = sandbox or build_runtime_sandbox()
    predicted: List[Dict[str, Any]] = []
    rollback_required = False

    for index, raw in enumerate(actions[:1000]):
        result = execute_runtime_action(raw, sandbox=sandbox, tick=tick + index)
        if result.get("executed"):
            predicted.append({
                "kind": str(raw.get("type", "action")),
                "target": str(raw.get("selector", raw.get("window", raw.get("command", "")))),
                "tick": tick + index,
            })
        else:
            rollback_required = True

    mutation_view = track_runtime_mutations(mutation={"kind": "simulated", "target": "dry_run", "tick": tick})

    return {
        "simulated": True,
        "predicted_mutations": predicted,
        "rollback_required": rollback_required,
        "mutation_preview": mutation_view.get("mutations", []),
        "runtime_mutated": False,
        "bounded": True,
    }
