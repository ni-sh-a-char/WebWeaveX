from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.execution_runtime_ir import (
    compile_execution_runtime_ir,
    execution_runtime_ir_to_graph,
)
from core.execution.runtime_checkpoint_engine import (
    load_execution_checkpoint,
    save_execution_checkpoint,
)
from core.execution.runtime_coordination_engine import coordinate_runtime_execution
from core.execution.runtime_execution_engine import execute_runtime_action
from core.execution.runtime_federation_engine import federate_runtime_execution
from core.execution.runtime_mutation_engine import track_runtime_mutations
from core.execution.runtime_policy_engine import build_runtime_policy, enforce_runtime_policy
from core.execution.runtime_permissions_engine import build_runtime_permissions
from core.execution.runtime_queue_engine import dequeue_runtime_action, enqueue_runtime_action
from core.execution.runtime_recovery_engine import recover_runtime_execution
from core.execution.runtime_replay_engine import replay_runtime_execution
from core.execution.runtime_rollback_engine import rollback_runtime_state
from core.execution.runtime_sandbox_engine import build_runtime_sandbox
from core.execution.runtime_scheduler_engine import schedule_runtime_execution
from core.execution.runtime_simulation_engine import simulate_runtime_execution
from core.execution.runtime_state_engine import build_execution_state
from core.execution.runtime_transaction_engine import (
    begin_runtime_transaction,
    commit_runtime_transaction,
)
from core.execution.runtime_transition_engine import apply_runtime_transition


def _default_actions(runtime: str) -> List[Dict[str, Any]]:
    if runtime == "native":
        return [{"type": "native_focus", "window": "application"}]
    if runtime == "terminal":
        return [{"type": "terminal_command", "command": "pwd"}]
    return [{"type": "browser_click", "selector": "#submit"}]


def run_execution_runtime(
    sources: Optional[Dict[str, Any]] = None,
    stored: Optional[Dict[str, Any]] = None,
    workers: Optional[List[Dict[str, Any]]] = None,
    runtime: str = "browser",
    tick: int = 0,
    simulate: bool = False,
    rollback_enabled: bool = True,
) -> Dict[str, Any]:
    sources = sources or {}
    stored = dict(stored or {})
    workers = list(workers or [{"worker_id": "primary", "runtime": runtime, "synced": True}])

    sandbox = build_runtime_sandbox(runtime=runtime)
    policy = build_runtime_policy(allow_terminal=runtime == "terminal")
    permissions = build_runtime_permissions(
        scopes=["browser", "native", "terminal", "connector", "vm"] if runtime == "browser" else [runtime],
    )

    prior_checkpoint = stored.get("checkpoint", {})
    checkpoint_body = prior_checkpoint.get("state", prior_checkpoint) if prior_checkpoint else {}

    raw_actions = sources.get("actions") or _default_actions(runtime)
    executed_actions: List[Dict[str, Any]] = []
    mutation_count = 0

    queue: List[Dict[str, Any]] = []
    for raw in raw_actions[: int(sandbox.get("max_actions", 1000))]:
        enqueue_result = enqueue_runtime_action(queue, raw, priority=0)
        queue = enqueue_result["queue"]

    if simulate:
        simulation = simulate_runtime_execution(raw_actions, sandbox=sandbox, tick=tick)
        transition = apply_runtime_transition("idle", "simulate")
        payload = {
            "simulation": simulation,
            "transition": transition,
            "sandbox": sandbox,
            "bounded": True,
        }
        payload["execution_ir"] = compile_execution_runtime_ir(payload)
        return payload

    transaction = begin_runtime_transaction(tick=tick)
    transition = apply_runtime_transition("idle", "enqueue")

    while queue:
        dequeue_result = dequeue_runtime_action(queue)
        queue = dequeue_result["queue"]
        action_raw = dequeue_result.get("action")
        if not action_raw:
            break

        raw = action_raw.get("action", action_raw)
        result = execute_runtime_action(
            raw,
            sandbox=sandbox,
            policy=policy,
            permissions=permissions,
            tick=tick,
            mutation_count=mutation_count,
            action_count=len(executed_actions),
        )
        if result.get("executed"):
            executed_actions.append(result.get("action", {}))
            mutation_count += 1
            track_result = track_runtime_mutations(
                prior=transaction.get("mutations", []),
                mutation={
                    "kind": str(result.get("runtime", "action")),
                    "target": str(result.get("action_id", "")),
                    "tick": tick,
                },
            )
            transaction["mutations"] = track_result.get("mutations", [])
            transaction["actions"] = executed_actions

        transition = apply_runtime_transition(transition["to"], "execute")

    transaction = commit_runtime_transaction(transaction)
    transition = apply_runtime_transition(transition["to"], "commit")

    mutations = track_runtime_mutations(prior=transaction.get("mutations", []))
    federation = federate_runtime_execution(workers, executed_actions)
    schedule = schedule_runtime_execution(executed_actions, tick=tick)
    coordination = coordinate_runtime_execution(
        [],
        federation,
        workflow=sources.get("workflow"),
        sync_state=sources.get("sync"),
    )

    rollback_result = {}
    if rollback_enabled and checkpoint_body:
        rollback_result = rollback_runtime_state(checkpoint_body, build_execution_state(runtime=runtime))

    recovery = recover_runtime_execution(
        failed_actions=[a for a in executed_actions if not a],
        checkpoint=checkpoint_body,
        interrupted_workflows=[sources.get("workflow")] if sources.get("workflow") else [],
    )

    state = build_execution_state(
        runtime=runtime,
        active_actions=executed_actions,
        queue=queue,
        mutations=mutations.get("mutations", []),
        checkpoint=checkpoint_body,
        transaction=transaction,
        federation=federation,
    )

    replay = replay_runtime_execution(
        executed_actions,
        transactions=[transaction],
        mutations=mutations.get("mutations", []),
        tick=tick,
    )

    payload = {
        "actions": executed_actions,
        "queue": {"queue": queue, "size": len(queue)},
        "transactions": [transaction],
        "mutations": mutations,
        "checkpoints": [checkpoint_body] if checkpoint_body else [],
        "federation": federation,
        "synchronization": sources.get("sync", {}),
        "state": state,
        "coordination": coordination,
        "schedule": schedule,
        "sandbox": sandbox,
        "policy": policy,
        "permissions": permissions,
        "rollback": rollback_result,
        "recovery": recovery,
        "replay": replay,
        "transition": transition,
        "bounded": True,
    }
    payload["execution_ir"] = compile_execution_runtime_ir(payload)
    return payload


def run_execution_for_extraction(
    execution_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    sources: Optional[Dict[str, Any]] = None,
    workers: Optional[List[Dict[str, Any]]] = None,
    runtime: str = "browser",
    tick: int = 0,
    simulate_execution: bool = False,
    rollback_enabled: bool = True,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not execution_runtime:
        return {"enabled": False, "bounded": True}

    stored: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_execution_checkpoint(memory_path, memory_key)
        if loaded.get("available"):
            stored = loaded.get("checkpoint", stored)

    result = run_execution_runtime(
        sources=sources,
        stored=stored,
        workers=workers,
        runtime=runtime,
        tick=tick,
        simulate=simulate_execution,
        rollback_enabled=rollback_enabled,
    )

    store = {
        "checkpoint": {
            "state": result.get("state", {}),
            "transactions": result.get("transactions", []),
            "mutations": result.get("mutations", {}),
            "workflows": sources.get("workflow", {}) if sources else {},
            "synchronization": result.get("synchronization", {}),
            "queues": [result.get("queue", {})],
        },
        "bounded": True,
    }

    persisted = False
    if memory_path and memory_key and not simulate_execution:
        save_execution_checkpoint(memory_path, store, memory_key)
        persisted = True

    graph_ir = execution_runtime_ir_to_graph(result.get("execution_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "execution": result,
        "execution_ir": result.get("execution_ir", {}),
        "execution_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "simulation": result.get("simulation", {}),
        "execution_persisted": persisted,
        "bounded": True,
    }
