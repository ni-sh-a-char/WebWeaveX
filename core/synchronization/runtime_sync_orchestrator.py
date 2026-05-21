from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir.synchronization_runtime_ir import (
    compile_synchronization_runtime_ir,
    synchronization_runtime_ir_to_graph,
)
from core.synchronization.reality_replication_engine import replicate_runtime_reality
from core.synchronization.runtime_alignment_engine import align_runtime_layers
from core.synchronization.runtime_continuity_engine import maintain_runtime_continuity
from core.synchronization.runtime_convergence_engine import converge_runtime_state
from core.synchronization.runtime_delta_engine import build_runtime_delta
from core.synchronization.runtime_diff_engine import diff_runtime_state
from core.synchronization.runtime_drift_engine import detect_runtime_drift
from core.synchronization.runtime_federation_engine import federate_runtime_realities
from core.synchronization.runtime_history_engine import build_runtime_history
from core.synchronization.runtime_merge_engine import merge_runtime_realities
from core.synchronization.runtime_mutation_engine import track_runtime_mutations
from core.synchronization.runtime_replay_engine import replay_synchronized_runtime
from core.synchronization.runtime_snapshot_engine import capture_runtime_snapshot
from core.synchronization.runtime_state_graph_engine import build_runtime_state_graph
from core.synchronization.runtime_sync_engine import synchronize_runtime
from core.synchronization.runtime_sync_memory_engine import load_sync_memory
from core.synchronization.runtime_sync_memory_engine import remember_sync_runtime
from core.synchronization.runtime_sync_memory_engine import save_sync_memory
from core.synchronization.runtime_consistency_engine import verify_runtime_consistency
from core.synchronization.runtime_timeline_engine import build_sync_timeline


def _runtime_view(
    extraction: Optional[Dict[str, Any]] = None,
    semantic: Optional[Dict[str, Any]] = None,
    workflow: Optional[Dict[str, Any]] = None,
    causality: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "dom": (extraction or {}).get("dom", {}),
        "semantic": (semantic or {}).get("semantic", semantic or {}),
        "workflow": (workflow or {}).get("workflow", workflow or {}),
        "causality": (causality or {}).get("causality", causality or {}),
        "runtime": (extraction or {}).get("runtime", {}),
    }


def run_synchronized_runtime(
    tick: int = 0,
    browser: Optional[Dict[str, Any]] = None,
    native: Optional[Dict[str, Any]] = None,
    semantic_result: Optional[Dict[str, Any]] = None,
    workflow_result: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    session: Optional[Dict[str, Any]] = None,
    identity: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    workers: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    memory = dict(memory or {})
    workers = list(workers or (distributed_result or {}).get("workers", []))

    previous_view = memory.get("last_view", {})
    current_view = _runtime_view(browser, semantic_result, workflow_result, causality_result)

    delta = build_runtime_delta(previous_view, current_view, tick=tick)
    snapshot = capture_runtime_snapshot(
        browser=browser,
        native=native,
        semantic=semantic_result,
        workflow=workflow_result,
        causality=causality_result,
        sync_state=memory.get("continuity", {}),
        tick=tick,
    )

    drift = detect_runtime_drift(
        {
            "selectors": previous_view.get("dom", {}),
            "semantic": previous_view.get("semantic", {}),
            "workflow": previous_view.get("workflow", {}),
            "topology": previous_view.get("runtime", {}),
            "application": previous_view.get("workflow", {}),
            "runtime": previous_view.get("runtime", {}),
        },
        {
            "selectors": current_view.get("dom", {}),
            "semantic": current_view.get("semantic", {}),
            "workflow": current_view.get("workflow", {}),
            "topology": current_view.get("runtime", {}),
            "application": current_view.get("workflow", {}),
            "runtime": current_view.get("runtime", {}),
        },
    )

    state_diff = diff_runtime_state(previous_view, current_view)
    mutations = track_runtime_mutations(delta.get("changes", []), tick=tick)

    realities = [
        {
            "reality_id": "primary",
            "tick": tick,
            "semantic": current_view.get("semantic", {}),
            "workflow": current_view.get("workflow", {}),
            "application": current_view.get("workflow", {}),
        }
    ]
    if distributed_result:
        realities.append({
            "reality_id": "distributed",
            "tick": tick,
            "semantic": {},
            "workflow": distributed_result,
            "application": {},
        })

    merged = merge_runtime_realities(realities)
    convergence = converge_runtime_state(realities)
    synchronization = synchronize_runtime([snapshot], tick=tick)
    replication = replicate_runtime_reality(
        {
            "reality_id": "primary",
            "semantic_state": current_view.get("semantic", {}),
            "runtime_state": current_view.get("runtime", {}),
            "workflows": current_view.get("workflow", {}),
            "checkpoints": memory.get("checkpoints", []),
            "causality_graph": current_view.get("causality", {}),
        },
        workers,
    )
    federation = federate_runtime_realities(
        workers=workers,
        browser=browser,
        native=native,
        semantic=semantic_result,
        application=workflow_result,
    )
    alignment = align_runtime_layers(browser, native, semantic_result, workflow_result)
    continuity = maintain_runtime_continuity(
        session=session,
        identity=identity,
        workflow=workflow_result,
        semantic=semantic_result,
        checkpoint=memory.get("checkpoint", {}),
    )

    prior_deltas = list(memory.get("deltas", []))
    all_deltas = prior_deltas + [delta]
    history = build_runtime_history(all_deltas, workflows=[merged.get("workflow", {})])
    timeline = build_sync_timeline(history)
    state_graph = build_runtime_state_graph(snapshot, delta, convergence)

    payload = {
        "snapshot": snapshot,
        "delta": delta,
        "drift": drift,
        "diff": state_diff,
        "mutations": mutations,
        "merge": merged,
        "convergence": convergence,
        "synchronization": synchronization,
        "replication": replication,
        "federation": federation,
        "alignment": alignment,
        "continuity": continuity,
        "history": history,
        "timeline": timeline,
        "state_graph": state_graph,
        "bounded": True,
    }

    updated_memory = remember_sync_runtime(
        memory,
        {
            "deltas": all_deltas,
            "history": history,
            "timeline": timeline,
            "convergence": convergence,
            "realities": realities,
            "continuity": continuity,
            "state_graph": state_graph,
            "last_view": current_view,
        },
    )
    replay = replay_synchronized_runtime(updated_memory)
    consistency = verify_runtime_consistency(history, convergence, replay)

    payload["memory"] = updated_memory
    payload["replay"] = replay
    payload["consistency"] = consistency
    payload["sync_ir"] = compile_synchronization_runtime_ir(payload)
    return payload


def run_sync_for_extraction(
    synchronized_runtime: bool = True,
    memory_path: str = "",
    memory_key: str = "",
    tick: int = 0,
    browser: Optional[Dict[str, Any]] = None,
    native: Optional[Dict[str, Any]] = None,
    semantic_result: Optional[Dict[str, Any]] = None,
    workflow_result: Optional[Dict[str, Any]] = None,
    causality_result: Optional[Dict[str, Any]] = None,
    distributed_result: Optional[Dict[str, Any]] = None,
    session: Optional[Dict[str, Any]] = None,
    identity: Optional[Dict[str, Any]] = None,
    merge_graph: bool = True,
) -> Dict[str, Any]:
    if not synchronized_runtime:
        return {"enabled": False, "bounded": True}

    memory: Dict[str, Any] = {}
    if memory_path and memory_key:
        loaded = load_sync_memory(memory_path, memory_key)
        if loaded.get("available"):
            memory = loaded.get("memory", memory)

    result = run_synchronized_runtime(
        tick=tick,
        browser=browser,
        native=native,
        semantic_result=semantic_result,
        workflow_result=workflow_result,
        causality_result=causality_result,
        distributed_result=distributed_result,
        session=session,
        identity=identity,
        memory=memory,
    )

    persisted = False
    if memory_path and memory_key:
        save_sync_memory(memory_path, result.get("memory", {}), memory_key)
        persisted = True

    graph_ir = synchronization_runtime_ir_to_graph(result.get("sync_ir", {}))
    unified_graph = {}
    if merge_graph:
        from core.runtime_graph.runtime_graph_engine import build_runtime_graph

        unified_graph = build_runtime_graph([graph_ir])

    return {
        "enabled": True,
        "synchronization": result,
        "sync_ir": result.get("sync_ir", {}),
        "sync_graph_ir": graph_ir,
        "unified_graph": unified_graph,
        "replay": result.get("replay", {}),
        "memory_persisted": persisted,
        "bounded": True,
    }
