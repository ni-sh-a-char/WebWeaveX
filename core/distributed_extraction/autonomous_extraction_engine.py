from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.distributed_extraction.distributed_checkpoint_engine import (
    load_distributed_checkpoint,
    save_distributed_checkpoint,
)
from core.distributed_extraction.distributed_extraction_orchestrator import (
    run_distributed_extraction,
)


def run_autonomous_extraction(
    tasks: List[Dict[str, Any]],
    workers: Optional[List[Dict[str, Any]]] = None,
    checkpoint_path: str = "",
    checkpoint_key: str = "",
    tick: int = 0,
    objective_execution: bool = False,
    objective_name: str = "monitor_metrics",
    native_extraction: bool = False,
    native_runtime: str = "desktop",
    causal_runtime: bool = False,
    semantic_runtime: bool = False,
    autonomous_workflow: bool = False,
    workflow_federation: bool = False,
    synchronized_runtime: bool = False,
    evolving_runtime: bool = False,
    evolution_memory_path: str = "",
    evolution_memory_key: str = "",
    live_runtime: bool = False,
    live_memory_path: str = "",
    live_memory_key: str = "",
    live_snapshot: Optional[Dict[str, Any]] = None,
    federated_memory: bool = False,
    federated_memory_path: str = "",
    federated_memory_key: str = "",
    execution_runtime: bool = False,
    execution_memory_path: str = "",
    execution_memory_key: str = "",
    simulate_execution: bool = False,
    rollback_enabled: bool = True,
    reconstruction_runtime: bool = False,
    reconstruction_memory_path: str = "",
    reconstruction_memory_key: str = "",
    fabricate_runtime: bool = False,
    clone_runtime: bool = False,
) -> Dict[str, Any]:
    checkpoint = {}

    if checkpoint_path and checkpoint_key:
        loaded = load_distributed_checkpoint(checkpoint_path, checkpoint_key)
        if loaded.get("available"):
            checkpoint = loaded.get("checkpoint", {})

    result = run_distributed_extraction(
        tasks=tasks,
        workers=workers,
        checkpoint=checkpoint,
        tick=tick,
    )

    if checkpoint_path and checkpoint_key:
        save_distributed_checkpoint(
            checkpoint_path,
            result.get("checkpoint", {}),
            checkpoint_key,
        )

    payload = {
        **result,
        "autonomous": True,
        "bounded": True,
    }

    if objective_execution:
        from core.application.runtime_goal_engine import build_runtime_goal

        payload["objective_execution"] = {
            "enabled": True,
            "objective": objective_name,
            "goal": build_runtime_goal(objective_name),
            "bounded": True,
        }

    if native_extraction:
        from core.native.native_runtime_orchestrator import extract_native

        native_agents = []
        for task in tasks[:1000]:
            application = str(task.get("application", task.get("app", "")))
            runtime = str(task.get("native_runtime", native_runtime))
            native_agents.append({
                "task_id": task.get("task_id", ""),
                "runtime": runtime,
                "application": application,
                "result": extract_native(
                    runtime=runtime,
                    application=application or "desktop",
                    application_cognition=False,
                    persistent_runtime=False,
                    merge_runtime_graph=False,
                ),
            })

        payload["native_extraction"] = {
            "enabled": True,
            "agents": native_agents,
            "bounded": True,
        }

    if causal_runtime:
        from core.causality.causality_orchestrator import run_causality_for_extraction

        worker_events = []
        for index, task in enumerate(tasks[:1000]):
            worker_events.append({
                "id": f"worker:evt:{index}",
                "runtime": "distributed",
                "type": "task",
                "step": index,
                "worker_id": str(task.get("task_id", f"worker_{index}")),
            })

        causality = run_causality_for_extraction(
            causality_runtime=True,
            distributed_result=payload,
            interactions=worker_events,
            merge_graph=False,
        )

        payload["causal_runtime"] = {
            "enabled": True,
            "propagation": causality.get("causality", {}).get("propagation", {}),
            "synchronization": causality.get("causality", {}).get("alignment", {}),
            "causal_graph": causality.get("causal_ir", {}),
            "bounded": True,
        }

    if semantic_runtime:
        from core.semantic.semantic_orchestrator import run_semantic_for_extraction

        semantics = run_semantic_for_extraction(
            semantic_runtime=True,
            url=str(tasks[0].get("url", "")) if tasks else "",
            html=" ".join(
                str(task.get("objective", task.get("url", "")))
                for task in tasks[:100]
            ),
            objective=objective_name,
            merge_graph=False,
        )

        payload["semantic_runtime"] = {
            "enabled": True,
            "domain": semantics.get("semantic", {}).get("domain", {}),
            "ontology": semantics.get("semantic_ir", {}).get("ontology", {}),
            "workflow_intent": semantics.get("semantic", {}).get("workflow", {}),
            "bounded": True,
        }

    if autonomous_workflow or workflow_federation:
        from core.workflows.workflow_orchestrator import run_workflow_for_extraction

        workflow = run_workflow_for_extraction(
            autonomous_workflow=True,
            objective=objective_name,
            distributed_result=payload,
            semantic_runtime=payload.get("semantic_runtime"),
            causality_result=payload.get("causal_runtime"),
            merge_graph=False,
        )

        payload["workflow_federation"] = {
            "enabled": True,
            "federation": workflow.get("workflow", {}).get("federation", {}),
            "execution": workflow.get("workflow", {}).get("execution", {}),
            "schedule": workflow.get("workflow", {}).get("schedule", {}),
            "bounded": True,
        }

    if synchronized_runtime:
        from core.synchronization.runtime_sync_orchestrator import run_sync_for_extraction

        sync = run_sync_for_extraction(
            synchronized_runtime=True,
            tick=tick,
            distributed_result=payload,
            semantic_result=payload.get("semantic_runtime"),
            workflow_result=payload.get("workflow_federation"),
            causality_result=payload.get("causal_runtime"),
            merge_graph=False,
        )

        payload["synchronized_runtime"] = {
            "enabled": True,
            "convergence": sync.get("synchronization", {}).get("convergence", {}),
            "replication": sync.get("synchronization", {}).get("replication", {}),
            "continuity": sync.get("synchronization", {}).get("continuity", {}),
            "bounded": True,
        }

    if evolving_runtime:
        from core.evolution_runtime.runtime_evolution_orchestrator import (
            run_evolution_for_extraction,
        )

        evolution = run_evolution_for_extraction(
            evolving_runtime=True,
            memory_path=evolution_memory_path,
            memory_key=evolution_memory_key,
            workflow_result=payload.get("workflow_federation"),
            semantic_result=payload.get("semantic_runtime"),
            sync_result=payload.get("synchronized_runtime"),
            distributed_result=payload,
            tick=tick,
            merge_graph=False,
        )

        payload["distributed_evolution"] = {
            "enabled": True,
            "convergence": evolution.get("evolution", {}).get("convergence", {}),
            "selector": evolution.get("evolution", {}).get("selector", {}),
            "shared_lineage": evolution.get("evolution", {}).get("lineage", []),
            "bounded": True,
        }

    if live_runtime:
        from core.connectors.live_runtime_orchestrator import run_live_for_extraction

        live = run_live_for_extraction(
            live_runtime=True,
            memory_path=live_memory_path,
            memory_key=live_memory_key,
            snapshot=live_snapshot,
            tick=tick,
            merge_graph=False,
        )

        payload["live_runtime_agents"] = {
            "enabled": True,
            "topology": live.get("live", {}).get("graph", {}),
            "kubernetes": live.get("live", {}).get("kubernetes", {}),
            "telemetry": live.get("live", {}).get("telemetry", {}),
            "streams": live.get("live", {}).get("streams", {}),
            "bounded": True,
        }

    if federated_memory:
        from core.memory.runtime_memory_orchestrator import run_memory_for_extraction

        memory = run_memory_for_extraction(
            federated_memory=True,
            memory_path=federated_memory_path,
            memory_key=federated_memory_key,
            sources={
                "workflow": payload.get("workflow_federation"),
                "semantic": payload.get("semantic_runtime"),
                "sync": payload.get("synchronized_runtime"),
                "evolution": payload.get("distributed_evolution"),
                "live": payload.get("live_runtime_agents"),
                "distributed": payload,
            },
            tick=tick,
            nodes=[{"node_id": str(t.get("task_id", ""))} for t in tasks[:100]],
            merge_graph=False,
        )

        payload["federated_memory"] = {
            "enabled": True,
            "memory_id": memory.get("memory", {}).get("runtime", {}).get("memory_id", ""),
            "lineage": memory.get("memory", {}).get("lineage", {}),
            "convergence": memory.get("memory", {}).get("convergence", {}),
            "bounded": True,
        }

    if execution_runtime:
        from core.execution.runtime_execution_orchestrator import run_execution_for_extraction

        execution = run_execution_for_extraction(
            execution_runtime=True,
            memory_path=execution_memory_path,
            memory_key=execution_memory_key,
            sources={
                "workflow": payload.get("workflow_federation"),
                "semantic": payload.get("semantic_runtime"),
                "sync": payload.get("synchronized_runtime"),
                "evolution": payload.get("distributed_evolution"),
                "live": payload.get("live_runtime_agents"),
                "memory": payload.get("federated_memory"),
            },
            workers=[{"worker_id": str(t.get("task_id", "")), "runtime": "browser"} for t in tasks[:100]],
            runtime="browser",
            tick=tick,
            simulate_execution=simulate_execution,
            rollback_enabled=rollback_enabled,
            merge_graph=False,
        )

        payload["execution_runtime"] = {
            "enabled": True,
            "federation": execution.get("execution", {}).get("federation", {}),
            "coordination": execution.get("execution", {}).get("coordination", {}),
            "simulation": execution.get("simulation", {}),
            "replay": execution.get("replay", {}),
            "bounded": True,
        }

    if reconstruction_runtime:
        from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_for_extraction

        reconstruction = run_reconstruction_for_extraction(
            reconstruction_runtime=True,
            memory_path=reconstruction_memory_path,
            memory_key=reconstruction_memory_key,
            sources={
                "semantic_ir": payload.get("semantic_runtime", {}),
                "workflow_ir": payload.get("workflow_federation", {}),
                "sync_ir": payload.get("synchronized_runtime", {}),
                "execution_ir": payload.get("execution_runtime", {}),
                "memory_ir": payload.get("federated_memory", {}),
                "workers": [{"worker_id": str(t.get("task_id", ""))} for t in tasks[:100]],
            },
            runtime_type="distributed",
            tick=tick,
            fabricate_runtime=fabricate_runtime,
            clone_runtime=clone_runtime,
            merge_graph=False,
        )

        payload["reconstruction_runtime"] = {
            "enabled": True,
            "runtime_id": reconstruction.get("reconstruction", {}).get("runtime", {}).get("runtime_id", ""),
            "validation": reconstruction.get("validation", {}),
            "replay": reconstruction.get("replay", {}),
            "fabrication": reconstruction.get("reconstruction", {}).get("fabrication", {}),
            "topology": reconstruction.get("reconstruction", {}).get("topology", {}),
            "bounded": True,
        }

    return payload
