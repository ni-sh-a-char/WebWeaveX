from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.workflow_runtime_ir import (
    compile_workflow_runtime_ir,
    workflow_runtime_ir_to_graph,
)
from core.workflows.objective_engine import build_runtime_objective
from core.workflows.workflow_alignment_engine import align_workflow_runtime
from core.workflows.workflow_dependency_engine import build_workflow_dependencies
from core.workflows.workflow_execution_engine import execute_workflow_plan
from core.workflows.workflow_federation_engine import federate_workflow_runtime
from core.workflows.workflow_memory_engine import load_workflow_memory
from core.workflows.workflow_memory_engine import remember_workflow_runtime
from core.workflows.workflow_memory_engine import save_workflow_memory
from core.workflows.workflow_navigation_engine import navigate_runtime_workflow
from core.workflows.workflow_planner_engine import build_workflow_plan
from core.workflows.workflow_recovery_engine import recover_workflow_runtime
from core.workflows.workflow_replay_engine import replay_workflow_runtime
from core.workflows.workflow_scheduler_engine import schedule_workflow_execution
from core.workflows.workflow_semantic_alignment_engine import align_workflow_semantics
from core.workflows.workflow_state_engine import build_workflow_state
from core.workflows.workflow_transition_engine import build_workflow_transitions
from core.workflows.workflow_graph_engine import build_workflow_graph
from core.workflows.workflow_runtime_engine import build_workflow_runtime_context


def run_autonomous_workflow(
    objective: str = "extract_dashboard",
    priority: int = 0,
    semantic_runtime: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    url: str = "",
    memory: Optional[Dict[str, Any]] = None,
    tick: int = 0,
    failures: Optional[List[str]] = None,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    runtime_objective = build_runtime_objective(objective, priority)

    semantic_inner = (semantic_runtime or {}).get("semantic", semantic_runtime or {})
    plan = build_workflow_plan(
        objective,
        semantic_runtime=semantic_inner,
        causality=causality_result,
        application_runtime=application_result,
    )
    plan["priority"] = priority

    execution = execute_workflow_plan(plan, tick=tick)
    state = build_workflow_state(plan, execution)
    navigation = navigate_runtime_workflow(plan, tick=tick)
    transitions = build_workflow_transitions(execution)
    dependencies = build_workflow_dependencies(plan)
    recovery = recover_workflow_runtime(state, failures)
    alignment = align_workflow_runtime(plan, state, execution)
    semantic_alignment = align_workflow_semantics(
        plan,
        semantic_runtime=semantic_runtime,
        causality=causality_result,
    )
    federation = federate_workflow_runtime(
        browser={"url": url},
        native=native_cognition,
        distributed=distributed_result,
        semantic=semantic_runtime,
        workers=(distributed_result or {}).get("workers", []),
    )
    schedule = schedule_workflow_execution([plan], tick=tick)
    context = build_workflow_runtime_context(
        url,
        runtime=plan["steps"][0]["runtime"] if plan.get("steps") else "browser",
        sources={
            "semantic": bool(semantic_runtime),
            "causality": bool(causality_result),
            "application": bool(application_result),
            "distributed": bool(distributed_result),
        },
    )
    workflow_graph = build_workflow_graph(
        runtime_objective,
        plan,
        state,
        execution,
        transitions,
    )

    payload = {
        "objective": runtime_objective,
        "plan": plan,
        "execution": execution,
        "state": state,
        "navigation": navigation,
        "transitions": transitions,
        "dependencies": dependencies,
        "recovery": recovery,
        "alignment": alignment,
        "semantic_alignment": semantic_alignment,
        "federation": federation,
        "schedule": schedule,
        "context": context,
        "workflow_graph": workflow_graph,
        "bounded": True,
    }

    updated_memory = remember_workflow_runtime(
        memory,
        {
            "objectives": runtime_objective,
            "workflow_states": state,
            "execution_graphs": execution,
            "semantic_checkpoints": [semantic_alignment],
            "runtime_transitions": transitions,
            "workflow_graph": workflow_graph,
        },
    )
    payload["memory"] = updated_memory
    payload["replay"] = replay_workflow_runtime(updated_memory)
    payload["workflow_ir"] = compile_workflow_runtime_ir(payload)
    return payload


def run_workflow_for_extraction(
    autonomous_workflow: bool = True,
    objective: str = "extract_dashboard",
    memory_path: str = "",
    memory_key: str = "",
    url: str = "",
    semantic_runtime: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    application_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    native_cognition: Optional[Dict[str, Any]] = None,
    merge_graph: bool = True,
    tick: int = 0,
) -> Dict[str, Any]:
    if not autonomous_workflow:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_workflow_memory(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_autonomous_workflow(
        objective=objective,
        semantic_runtime=semantic_runtime,
        causality_result=causality_result,
        application_result=application_result,
        distributed_result=distributed_result,
        native_cognition=native_cognition,
        url=url,
        memory=memory,
        tick=tick,
    )

    persisted = False
    if memory_path and memory_key:
        save_workflow_memory(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = workflow_runtime_ir_to_graph(result.get("workflow_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "workflow": result,
        "workflow_ir": result.get("workflow_ir", {}),
        "workflow_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }
